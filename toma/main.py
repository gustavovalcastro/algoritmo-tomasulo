from utils import *
import sys

reorder_buffer = new_reorder(8)
reservation_stations = new_reservation()
register_status = new_registers(8)
        

cycle = 0
branch = sys.argv[1]
next = "y"

reorder_buffer = fetch_instructions(reorder_buffer)

while next != "n":
    print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch)

    print("Continue? No [n] or Yes [any]: ")
    next = input()
    cycle += 1
