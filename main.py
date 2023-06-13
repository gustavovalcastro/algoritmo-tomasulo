from utils import *
import sys

reorder_buffer = new_reorder(10)
reservation_stations = new_reservation()
register_status = new_registers(10)
        

cycle = 0
branch = sys.argv[1]
next = "y"
flush = []

reorder_buffer = fetch_instructions(reorder_buffer, "")
dependencies = check_dependencies(reorder_buffer)
var_dependencies = check_dependencies(reorder_buffer)

print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch, "")

print("Continue? No [n] or Yes [any]: ")
next = input()

while next != "n":
    cycle += 1

    issue_registers(reorder_buffer, reservation_stations, var_dependencies)
    execute_instructions(reorder_buffer, reservation_stations)
    write_instructions(reorder_buffer, reservation_stations, dependencies, var_dependencies, register_status, cycle, branch)
    flush = commit_instructions(reorder_buffer, register_status, branch)
    print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch, "")

    if flush[0] == "flush":
        reorder_buffer = []
        reservation_stations = []
        register_status = []
        dependencies = []
        var_dependencies = []

        reorder_buffer = new_reorder(10)
        reservation_stations = new_reservation()
        register_status = new_registers(10)

        reorder_buffer = fetch_instructions(reorder_buffer, flush[1])
        dependencies = check_dependencies(reorder_buffer)
        var_dependencies = check_dependencies(reorder_buffer)
        flush = ["", ""]

        print_tables(reorder_buffer, reservation_stations, register_status, cycle, branch, "")

    # for i in dependencies:
        # i.print()

    print("Continue? No [n] or Yes [any]: ")
    next = input()
