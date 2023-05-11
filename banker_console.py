import gui
def request_resources(process_num, request, available, currently_allocated, max_need):
    resources = len(available)
    # Check if the request can be granted
    for i in range(resources):
        if request[i] > available[i]:
            print("Error: Requested resources exceed available resources.")
            return False
        if request[i] > max_need[process_num][i] - currently_allocated[process_num][i]:
            print("Error: Requested resources exceed maximum need of the process.")
            return False

    # Try to allocate the requested resources and check if the new state is safe
    for i in range(resources):
        available[i] -= request[i]
        currently_allocated[process_num][i] += request[i]

    if is_safe_state(available, currently_allocated, max_need):
        return True
    else:
        # The new state is not safe, so undo the allocation
        for i in range(resources):
            available[i] += request[i]
            currently_allocated[process_num][i] -= request[i]
        return False


def is_safe_state(available, currently_allocated, max_need):
    resources = len(available)
    running = [True] * len(currently_allocated)
    count = len(currently_allocated)
    while count != 0:
        safe = False
        for i in range(len(currently_allocated)):
            if running[i]:
                executing = True
                for j in range(resources):
                    if max_need[i][j] - currently_allocated[i][j] > available[j]:
                        executing = False
                        break
                if executing:
                    print(f"Process {i + 1} is executing")
                    running[i] = False
                    count -= 1
                    safe = True
                    for j in range(resources):
                        available[j] += currently_allocated[i][j]
                    break
        if not safe:
            print("The processes are in an unsafe state.")
            return False
    print("The processes are in a safe state.")
    return True


def main():
    processes = int(input("Number of processes: "))
    resources = int(input("Number of resources: "))
    max_resources = [int(i) for i in input("Maximum resources: ").split()]

    print("\n-- Allocated resources for each process --")
    currently_allocated = [[int(i) for i in input(f"Process {j + 1}: ").split()] for j in range(processes)]

    print("\n-- Maximum need of resources for each process --")
    max_need = [[int(i) for i in input(f"Process {j + 1}: ").split()] for j in range(processes)]

    allocated = [0] * resources
    for i in range(processes):
        for j in range(resources):
            allocated[j] += currently_allocated[i][j]
    print(f"\nTotal allocated resources: {allocated}")

    available = [max_resources[i] - allocated[i] for i in range(resources)]
    print(f"Total available resources: {available}\n")

    while True:
        command = input("Enter 'r' to request resources, 's' to show status, or 'q' to quit: ")
        if command == 'q':
            break
        elif command == 'r':
            process_num = int(input("Enter process number: ")) - 1
            request = [int(i) for i in input("Enter the request: ").split()]
            if request_resources(process_num, request, available, currently_allocated, max_need):
                print("Request granted.")
            else:
                print("Request denied.")
        elif command == 's':
            is_safe_state(available, currently_allocated, max_need)

    print("Program terminated.")


if __name__ == '__main__':
    main()
