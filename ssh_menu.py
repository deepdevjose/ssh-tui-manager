import os

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Set up the virtual machines and their users
vms = {
    "VM1": {
        "ip": "your.vm.ip",  # Replace with actual IP
        "usuarios": ["root", "your_user1"],
        "color": RED
    },
}

while True:
    print(f"\n{CYAN}=== SSH Menu ==={RESET}")
    for idx, (vm_name, vm_info) in enumerate(vms.items(), start=1):
        print(f"{idx}. {vm_info['color']}{vm_name}{RESET}")
    print(f"{len(vms)+1}. Exit")

    opcion_vm = input(f"{CYAN}Select the VM number:{RESET} ")

    if not opcion_vm.isdigit():
        print(f"{RED}Invalid option, please enter a number.{RESET}")
        continue

    opcion_vm = int(opcion_vm)
    if opcion_vm == len(vms) + 1:
        print(f"{CYAN}Exiting SSH menu. Goodbye!{RESET}")
        break
    elif opcion_vm < 1 or opcion_vm > len(vms):
        print(f"{RED}Invalid option, try again.{RESET}")
        continue

    vm_name = list(vms.keys())[opcion_vm - 1]
    vm_info = vms[vm_name]
    ip = vm_info["ip"]

    # List users for the selected VM
    print(f"\n{vm_info['color']}=== Users for {vm_name} ==={RESET}")
    for idx, user in enumerate(vm_info["usuarios"], start=1):
        print(f"{idx}. {user}")

    opcion_user = input(f"{CYAN}Select the user number:{RESET} ")

    if not opcion_user.isdigit() or int(opcion_user) < 1 or int(opcion_user) > len(vm_info["usuarios"]):
        print(f"{RED}Invalid user, try again.{RESET}")
        continue

    usuario = vm_info["usuarios"][int(opcion_user) - 1]

    # Open SSH connection in a new CMD window
    print(f"\n{vm_info['color']}Opening SSH to {vm_name} ({ip}) as {usuario} in a new window...{RESET}\n")
    os.system(f'start cmd /k ssh {usuario}@{ip}')
