import os
import sys

# Ansi escape codes for colored output
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Set up the virtual machines and their users
vms = {
    "VM1": {
        "ip": "your.vm.ip",  # Replace with actual IP
        "users": ["root", "your_user1"],
        "color": RED
    },
}

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')
while True:
    clear_screen()
    print(f"{CYAN}╔════════════════════════════════╗{RESET}")
    print(f"{CYAN}║        SSH MENU - WINDOWS      ║{RESET}")
    print(f"{CYAN}╚════════════════════════════════╝{RESET}\n")

    # Mostrar las VMs con colores
    for idx, (vm_name, vm_info) in enumerate(vms.items(), start=1):
        print(f" {idx}. {vm_info['color']}{vm_name}{RESET} ({vm_info['ip']})")
    print(f" {len(vms)+1}. {YELLOW}Exit{RESET}\n")

    opcion_vm = input(f"{CYAN}Select the VM number:{RESET} ")

    if not opcion_vm.isdigit():
        input(f"{RED}Invalid option, press Enter to continue...{RESET}")
        continue

    opcion_vm = int(opcion_vm)
    if opcion_vm == len(vms) + 1:
        clear_screen()
        print(f"{CYAN}Goodbye!{RESET}")
        sys.exit(0)
    elif opcion_vm < 1 or opcion_vm > len(vms):
        input(f"{RED}Invalid option, press Enter to continue...{RESET}")
        continue

    vm_name = list(vms.keys())[opcion_vm - 1]
    vm_info = vms[vm_name]
    ip = vm_info["ip"]

    # Submenú de usuarios
    clear_screen()
    print(f"{vm_info['color']}=== Users for {vm_name} ==={RESET}\n")
    for idx, user in enumerate(vm_info["users"], start=1):
        print(f" {idx}. {user}")

    opcion_user = input(f"\n{CYAN}Select the user number:{RESET} ")

    if not opcion_user.isdigit() or int(opcion_user) < 1 or int(opcion_user) > len(vm_info["usuarios"]):
        input(f"{RED}Invalid user, press Enter to continue...{RESET}")
        continue

    user = vm_info["users"][int(opcion_user) - 1]

    # Open SSH connection in a new CMD window
    clear_screen()
    print(f"{vm_info['color']}Opening SSH to {vm_name} ({ip}) as {user}...{RESET}\n")
    os.system(f'start cmd /k ssh {user}@{ip}')

    input(f"{CYAN}\nPress Enter to return to the menu...{RESET}")