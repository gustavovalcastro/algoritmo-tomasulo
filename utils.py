from os import system
from tabulate import tabulate
from instructions import *

class BufferEntry:
    def __init__(self, entry, busy, instruction, state, value, destination, flush_after):
        self.entry = entry
        self.busy = busy
        self.instruction = instruction
        self.state = state
        self.value = value
        self.destination = destination
        self.flush_after = flush_after

    def toArray(self):
        return [self.entry, self.busy, self.instruction.toString(), self.state, self.destination, self.value]

class ReservationEntry:
    def __init__(self, name, busy, op, vj, vk, qj, qk, dest, a, type, changed):
        self.name = name
        self.busy = busy
        self.op = op
        self.vj = vj
        self.vk = vk
        self.qj = qj
        self.qk = qk
        self.dest = dest
        self.a = a
        self.type = type
        self.changed = changed

    def toArray(self):
        return [self.name, self.busy, self.op, self.vj, self.vk, self.qj, self.qk, self.dest, self.a]
        # return [self.name, self.busy, self.op, self.vj, self.vk, self.qj, self.qk, self.dest, self.a, self.changed]

class RegisterEntry:
    def __init__(self, name, reorder_number, busy):
        self.name = name
        self.reorder_number = reorder_number
        self.busy = busy

    def toArray(self):
        return [self.name, self.reorder_number, self.busy]

def fetch_instructions(reorder_buffer):
    i = 0
    n = len(reorder_buffer) if len(reorder_buffer) < len(instructions) else len(instructions)

    for i in range(0, n):
        if instructions[i].op == "sw" or instructions[i].op == "bne":
            dest = ""
        else:
            dest = instructions[i].dest
        
        reorder_buffer[i] = BufferEntry(i, "Yes", instructions[i], "Issue", "", dest, "")

    return reorder_buffer


def new_reorder(entries):
    arr = []

    for i in range(0, entries):
        arr.append(BufferEntry(i, "No", Instruction("", "", "", "", "", "", 0), "", "", "", ""))
    
    return arr

def new_reservation():
    arr = []
    stations = ["Load1", "Load2", "Store1", "Store2", "Add1", "Add2", "Beq1"]
    stations_type = ["Load", "Load", "Store", "Store", "Add", "Add", "Beq"]

    i = 0
    for unity in stations:
        arr.append(ReservationEntry(unity, "No", "", "", "", "", "", "", "", stations_type[i], "No"))
        i += 1

    return arr


def new_registers(entries):
    arr = []

    for i in range(0, entries):
        arr.append(RegisterEntry("x{}".format(i), "", "No"))

    return arr

def access_mem(instr):
    return True if instr == "lw" or instr == "sw" else False

def to_regs(component):
    return "Regs[{}]".format(component)

def check_dependencies(reorder_buffer):
    dependencies = []
    
    for entry in reorder_buffer:
        dependencies.append(InstructionDependencies(entry.entry, "", "", ""))

    i = 0
    for entry in reorder_buffer:
        dest = entry.instruction.dest

        i += 1
        for j in range(i, len(reorder_buffer)):
            if entry.instruction.op == "sw": break

            if dest == reorder_buffer[j].instruction.vj and dependencies[j].vj == "":
                dependencies[j].vj = entry.entry
            if dest == reorder_buffer[j].instruction.vk and dependencies[j].vk == "":
                dependencies[j].vk = entry.entry
            if dest == reorder_buffer[j].instruction.dest and dependencies[j].dest == "":
                dependencies[j].dest = entry.entry
                break

    return dependencies

def reset_changes(reservation_stations):
    for station in reservation_stations:
        station.changed = "No"

def verify_issue(entry, station, dependencies, id):
    # Load
    if entry.instruction.checkType() == "Load":
        if dependencies[id].vk != "":
            station.qj = "#{}".format(dependencies[id].vk)
            station.a = entry.instruction.offset + ' + ' + "#{}".format(dependencies[id].vk)

            print(station.toArray())
        else:
            station.a = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vk)

    # Store
    elif entry.instruction.checkType() == "Store":
        if dependencies[id].vj != "":
            station.qk = "#{}".format(dependencies[id].vj)
        else:
            station.vk = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vj)
        if dependencies[id].vk != "":
            station.qj = "#{}".format(dependencies[id].vk)
        else:
            station.vj = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vk)

    # Add e Bne
    else:
        if dependencies[id].vj != "":
            station.qj = "#{}".format(dependencies[id].vj)
        else: 
            station.vj = to_regs(entry.instruction.vj)

        if dependencies[id].vk != "":
            station.qk = "#{}".format(dependencies[id].vk)
        else: 
            station.vk = to_regs(entry.instruction.vk)

def verify_execute(entry, station, dependencies, id):
    # Load
    if entry.instruction.checkType() == "Load":
        if dependencies[id].vk == "":
            station.qj = ""
            # station.a = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vk)

    # Store
    elif entry.instruction.checkType() == "Store":
        if dependencies[id].vj == "":
            station.qk = ""
            station.vk = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vj)
        if dependencies[id].vk == "":
            station.qj = ""
            station.vj = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vk)

    # Add e Bne
    else:
        if dependencies[id].vj == "":
            station.qj = ""
            station.vj = to_regs(entry.instruction.vj)

        if dependencies[id].vk == "":
            station.qk = ""
            station.vk = to_regs(entry.instruction.vk)

def issue_registers(reorder_buffer, reservation_stations, dependencies):
    reset_changes(reservation_stations)

    for id, entry in enumerate(reorder_buffer):
        if entry.state == "Issue":
            for station in reservation_stations:
                if station.type == entry.instruction.checkType() and station.busy == "No":
                    station.busy = "Yes"
                    station.op = entry.instruction.op
                    station.dest = "#{}".format(entry.entry)
                    station.changed = "Yes"

                    verify_issue(entry, station, dependencies, id)

                    entry.state = "Execute"
                    break

    return (reorder_buffer, reservation_stations)

def get_instruction(reorder_buffer, dest):
    instr = {"offset": "", "vj": "", "vk": "", "remaining_cycles": 0}

    for entry in reorder_buffer:
        if "#" + str(entry.entry) == dest:
            instr['entry'] = entry.entry
            instr['dest'] = entry.instruction.dest
            instr['offset'] = entry.instruction.offset
            instr['vj'] = entry.instruction.vj
            instr['vk'] = entry.instruction.vk
            instr['remaining_cycles'] = entry.instruction.remaining_cycles

    return instr

def exec(reorder_buffer, dest):
    for entry in reorder_buffer:
        if dest == entry.entry:
            # if entry.state == "Issue": entry.state = "Execute"
            entry.instruction.remaining_cycles -= 1

def execute_instructions(reorder_buffer, reservation_stations, dependencies):
    for station in reservation_stations:
        if station.busy == "Yes" and station.changed == "No":
            instr = get_instruction(reorder_buffer, station.dest)

            if station.op == "lw":
                if station.qj == "":
                    station.a = instr['offset'] + ' + ' + to_regs(instr['vk'])

                    if instr['remaining_cycles'] != 0:
                        exec(reorder_buffer, instr['entry'])
                        station.changed = "Yes"
            else:
                if station.qj == "" and station.qk == "":
                    if instr['remaining_cycles'] != 0:
                        exec(reorder_buffer, instr['entry'])
                        station.changed = "Yes"

def write(reorder_buffer, dest, dependencies, reservation_stations):
    for id, entry in enumerate(reorder_buffer):
        if dest == entry.entry:
            if entry.state == "Execute": entry.state = "Write Result"

            for instruction in dependencies:
                if instruction.vj == entry.entry: instruction.vj = ""
                if instruction.vk == entry.entry: instruction.vk = ""

            for station in reservation_stations:
                if station.type == entry.instruction.checkType() and station.busy == "Yes":
                    verify_execute(entry, station, dependencies, id)

def write_instructions(reorder_buffer, reservation_stations, dependencies):
    for id, station in enumerate(reservation_stations):
        if station.busy == "Yes" and station.changed == "No":
            instr = get_instruction(reorder_buffer, station.dest)

            if instr['remaining_cycles'] == 0:
                write(reorder_buffer, instr['entry'], dependencies, reservation_stations)
                reservation_stations[id] = ReservationEntry(station.name, "No", "", "", "", "", "", "", "", station.type, "Yes")

def print_horizontal(headers, data):
    i = 0
    dt = list(zip(*data))
    table_data = []

    for row in dt:
        table_data.append([headers[i]] + list(row))
        i += 1

    print(tabulate(table_data, tablefmt="plain"))

def get_array(obj):
    arr = []

    for element in obj:
        arr.append(element.toArray())    
    
    return arr

def print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch):
    system("clear")

    print("\033[1mCycle: {}\033[0m".format(cycle))
    print("\033[1mWill Branch? {}\033[0m".format(branch))
    print('\033[1m-\033[0m' * 100)
    print("\033[1m" + "Reorder Buffer" + "\033[0m")
    print(tabulate(get_array(reorder_buffer), headers=["Entry", "Busy", "Instruction", "State", "Destination", "Value"]))

    print('\033[1m-\033[0m' * 100)
    print("\033[1m" + "Reservation Station" + "\033[0m")
    print(tabulate(get_array(reservation_stations), headers=["Name", "Busy", "Op", "Vj", "Vk", "Qj", "Qk", "Dest", "A"]))

    print('\033[1m-\033[0m' * 100)
    print("\033[1m" + "Register Status" + "\033[0m")

    headers = ["Field", "Reorder Entry", "Busy"]
    print_horizontal(headers, get_array(register_status))
    print('\033[1m-\033[0m' * 100)


