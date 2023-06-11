from os import system
from tabulate import tabulate
from instructions import *

class BufferEntry:
    def __init__(self, entry, busy, instruction, state, value):
        self.entry = entry
        self.busy = busy
        self.instruction = instruction
        self.state = state
        self.value = value
        self.destination = self.instruction.dest

    def toArray(self):
        return [self.entry, self.busy, self.instruction.toString(), self.state, self.destination, self.value]

class ReservationEntry:
    def __init__(self, name, busy, op, vj, vk, qj, qk, dest, a):
        self.name = name
        self.busy = busy
        self.op = op
        self.vj = vj
        self.vk = vk
        self.qj = qj
        self.qk = qk
        self.dest = dest
        self.a = a

    def toArray(self):
        return [self.name, self.busy, self.op, self.vj, self.vk, self.qj, self.qk, self.dest, self.a]

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
        reorder_buffer[i] = BufferEntry(i, "Yes", instructions[i], "", "")

    return reorder_buffer


def new_reorder(entries):
    arr = []

    for i in range(0, entries):
        arr.append(BufferEntry(i, "No", Instruction("", "", "", "", ""), "", ""))
    
    return arr

def new_reservation():
    arr = []
    stations = ["Load1", "Load2", "Store1", "Store2", "Add1", "Add2", "Bne1"]

    for unity in stations:
        arr.append(ReservationEntry(unity, "No", "", "", "", "", "", "", ""))

    return arr


def new_registers(entries):
    arr = []

    for i in range(0, entries):
        arr.append(RegisterEntry("x{}".format(i), "", "No"))

    return arr

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


