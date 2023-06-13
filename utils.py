from os import system
from tabulate import tabulate
from instructions import *

class BufferEntry:
    def __init__(self, entry, busy, instruction, state, value, destination, flush_after, changed):
        self.entry = entry
        self.busy = busy
        self.instruction = instruction
        self.state = state
        self.value = value
        self.destination = destination
        self.flush_after = flush_after
        self.changed = changed

    def toArray(self):
        return [self.entry, self.busy, self.instruction.toString(), self.state, self.destination, self.value]
        # return [self.entry, self.busy, self.instruction.toString(), self.state, self.destination, self.value, self.flush_after]

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

def new_instructions():
    instr = []

    for i in instructions:
        instr.append(Instruction(i.op, i.dest, i.offset, i.vj, i.vk, i.label, i.remaining_cycles))

    return instr

def fetch_instructions(reorder_buffer, label):
    i = 0
    instructions_base = new_instructions()

    if label != "":
        for instruction in instructions_base:
            if instruction.label == label:
                break
            i += 1

        instr = instructions_base[i:]
        n = len(reorder_buffer) if len(reorder_buffer) < len(instr) else len(instr)

        for i in range(0, n):
            if instr[i].op == "sw" or instr[i].op == "bne":
                dest = ""
            else:
                dest = instr[i].dest
            
            reorder_buffer[i] = BufferEntry(i, "Yes", instr[i], "Issue", "", dest, "No", "No")
        
        return reorder_buffer

    n = len(reorder_buffer) if len(reorder_buffer) < len(instructions_base) else len(instructions_base)

    for i in range(0, n):
        if instructions_base[i].op == "sw" or instructions_base[i].op == "bne":
            dest = ""
        else:
            dest = instructions_base[i].dest
        
        reorder_buffer[i] = BufferEntry(i, "Yes", instructions_base[i], "Issue", "", dest, "No", "No")

    return reorder_buffer

def new_reorder(entries):
    arr = []

    for i in range(0, entries):
        arr.append(BufferEntry(i, "No", Instruction("", "", "", "", "", "", 0), "", "", "", "", ""))
    
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

def reset_changes(reorder_buffer, reservation_stations):
    for entry in reorder_buffer:
        entry.changed = "No"
    for station in reservation_stations:
        station.changed = "No"

def verify_issue(entry, station, dependencies, id):
    # Load
    if entry.instruction.checkType() == "Load":
        if dependencies[id].vk != "":
            station.qj = "#{}".format(dependencies[id].vk)
            station.a = entry.instruction.offset + ' + ' + "#{}".format(dependencies[id].vk)
        else:
            station.a = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vk)

    # Store
    elif entry.instruction.checkType() == "Store":
        if dependencies[id].vj != "":
            station.qj = "#{}".format(dependencies[id].vj)
        else:
            station.vj = to_regs(entry.instruction.vj)
        if dependencies[id].vk != "":
            station.qk = "#{}".format(dependencies[id].vk)
        else:
            station.vk = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vk)

    # Add e Bnei
    else:
        if dependencies[id].vj != "":
            station.qj = "#{}".format(dependencies[id].vj)
        else: 
            station.vj = to_regs(entry.instruction.vj)

        if dependencies[id].vk != "":
            station.qk = "#{}".format(dependencies[id].vk)
        else: 
            station.vk = to_regs(entry.instruction.vk)


def issue_registers(reorder_buffer, reservation_stations, dependencies):
    reset_changes(reorder_buffer, reservation_stations)

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

def exec(reorder_buffer, buff_entry):
    for id, entry in enumerate(reorder_buffer):
        if buff_entry == entry.entry:
            entry.instruction.remaining_cycles -= 1
            break

def execute_instructions(reorder_buffer, reservation_stations):
    for station in reservation_stations:
        # if station.busy == "Yes" and station.changed == "No":
        if station.busy == "Yes":
            instr = get_instruction(reorder_buffer, station.dest)

            if station.op == "lw":
                if station.qj == "":
                    station.a = instr['offset'] + ' + ' + to_regs(instr['vk'])

                    if instr['remaining_cycles'] > 0:
                        exec(reorder_buffer, instr['entry'])
                        station.changed = "Yes"
            else:
                if station.qj == "" and station.qk == "":
                    if instr['remaining_cycles'] > 0:
                        exec(reorder_buffer, instr['entry'])
                        station.changed = "Yes"

def verify_write(entry, station, dependencies, id):
    # Load
    if entry.instruction.checkType() == "Load" and station.type == "Load":
        if dependencies[id].vk == "":
            station.qj = ""
            # station.a = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vk)

    # Store
    elif entry.instruction.checkType() == "Store" and station.type == "Store":
        if dependencies[id].vj == "":
            station.qj = ""
            # station.vj = to_regs(entry.instruction.vk)
        if dependencies[id].vk == "":
            station.qk = ""
            # station.vk = to_regs(entry.instruction.vk)

    # Add e Bne
    else:
        if dependencies[id].vj == "":
            station.qj = ""

        if dependencies[id].vk == "":
            station.qk = ""

def to_entry(entry):
    return "#{}".format(entry)

def write(reorder_buffer, buff_entry, dependencies, var_dependencies, reservation_stations, register_status, cycle, branch):
    for id, entry in enumerate(reorder_buffer):
        if buff_entry == entry.entry:
            for register in register_status:
                if register.name == entry.destination:
                    register.reorder_number = buff_entry
                    register.busy = "Yes"

            entry.state = "Write Result"
            entry.changed = "Yes"

            for station in reservation_stations:
                if station.dest != "#{}".format(buff_entry):
                    if station.type == "Load":
                        if station.qj == "#{}".format(buff_entry):
                            station.qj = ""
                            # station.a = entry.instruction.offset + ' + ' + to_regs(entry.instruction.vk)
                    else:
                        if station.qj == "#{}".format(buff_entry):
                            station.qj = ""
                            station.vj = to_regs(entry.destination)
                        if station.qk == "#{}".format(buff_entry):
                            station.qk = ""
                            station.vk = to_regs(entry.destination)

            if entry.instruction.op == "lw":
                if dependencies[entry.entry].vk == "":
                    entry.value = "Mem[{} + Regs[{}]]".format(entry.instruction.offset, entry.instruction.vk)
                else:
                    entry.value = "Mem[{} + #{}]".format(entry.instruction.offset, dependencies[entry.entry].vk)

            elif entry.instruction.op == "sw":
                entry.value = "{}".format(to_regs(entry.instruction.vj) if dependencies[entry.entry].vj == "" else to_entry(dependencies[entry.entry].vj)) 
                entry.destination = "Mem[{} + {}]".format(entry.instruction.offset, 
                                                          to_regs(entry.instruction.vk) if dependencies[entry.entry].vk == "" else to_entry(dependencies[entry.entry].vk)) 

            elif entry.instruction.op == "add":
                entry.value = "{} + {}".format(
                    to_regs(entry.instruction.vj) if dependencies[entry.entry].vj == "" else to_entry(dependencies[entry.entry].vj), 
                    to_regs(entry.instruction.vk) if dependencies[entry.entry].vk == "" else to_entry(dependencies[entry.entry].vk), entry.instruction.vk)
            elif entry.instruction.op == "sub":
                entry.value = "{} - {}".format(
                    to_regs(entry.instruction.vj) if dependencies[entry.entry].vj == "" else to_entry(dependencies[entry.entry].vj), 
                    to_regs(entry.instruction.vk) if dependencies[entry.entry].vk == "" else to_entry(dependencies[entry.entry].vk), entry.instruction.vk)
            elif entry.instruction.op == "mul":
                entry.value = "{} x {}".format(
                    to_regs(entry.instruction.vj) if dependencies[entry.entry].vj == "" else to_entry(dependencies[entry.entry].vj), 
                    to_regs(entry.instruction.vk) if dependencies[entry.entry].vk == "" else to_entry(dependencies[entry.entry].vk), entry.instruction.vk)
            elif entry.instruction.op == "div":
                entry.value = "{} / {}".format(
                    to_regs(entry.instruction.vj) if dependencies[entry.entry].vj == "" else to_entry(dependencies[entry.entry].vj), 
                    to_regs(entry.instruction.vk) if dependencies[entry.entry].vk == "" else to_entry(dependencies[entry.entry].vk), entry.instruction.vk)
            elif entry.instruction.op == "bne":
                if entry.entry > 0:
                    reorder_buffer[entry.entry - 1].flush_after = branch
                    if branch == "Yes":
                        print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch, "[WARNING] Waiting for previous instruction to commit in order to branch")

                        print("Continue? No [n] or Yes [any]: ")
                        next = input()

            for instruction in var_dependencies:
                if instruction.vj == entry.entry: instruction.vj = ""
                if instruction.vk == entry.entry: instruction.vk = ""

def write_instructions(reorder_buffer, reservation_stations, dependencies, var_dependencies, register_status, cycle, branch):
    for id, station in enumerate(reservation_stations):
        # if station.busy == "Yes" and station.changed == "No":
        if station.busy == "Yes":
            instr = get_instruction(reorder_buffer, station.dest)

            if instr['remaining_cycles'] <= 0:
                write(reorder_buffer, instr['entry'], dependencies, var_dependencies, reservation_stations, register_status, cycle, branch)
                reservation_stations[id] = ReservationEntry(station.name, "No", "", "", "", "", "", "", "", station.type, "Yes")

def commit(entry, register_status):
    entry.state = "Commit"

    for register in register_status:
        if register.reorder_number == entry.entry:
            register.reorder_number = ""
            register.busy = "No"

    if entry.flush_after == "Yes": return "flush"
    else: return ""

def commit_instructions(reorder_buffer, register_status, branch): 
    for entry in reorder_buffer:
        if entry.state == "Commit":
            continue

        if entry.state == "Write Result":
            if entry.changed == "No":
                if branch == "Yes": res = reorder_buffer[entry.entry + 1].instruction.dest
                else: res = ""
                return [commit(entry, register_status), res]
        
        return ["", ""]

    return ["", ""]

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

def print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch, right_before):
    system("clear")

    print("\033[1mCycle: {}\033[0m".format(cycle))
    print("\033[1mWill Branch? {}\033[0m".format(branch))
    print("\033[1m{}\033[0m".format(right_before))
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


