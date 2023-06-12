from utils import *
import sys

reorder_buffer = new_reorder(8)
reservation_stations = new_reservation()
register_status = new_registers(8)
        

cycle = 0
branch = sys.argv[1]
next = "y"

reorder_buffer = fetch_instructions(reorder_buffer)
dependencies = check_dependencies(reorder_buffer)

print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch)

print("Continue? No [n] or Yes [any]: ")
next = input()

while next != "n":
    cycle += 1

    issue_registers(reorder_buffer, reservation_stations, dependencies)
    execute_instructions(reorder_buffer, reservation_stations, dependencies)
    write_instructions(reorder_buffer, reservation_stations, dependencies)
    print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch)

    # for i in dependencies:
    #     i.print()

    print("Continue? No [n] or Yes [any]: ")
    next = input()
