import os
import sys
import json

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

CONFIG_FILE = "vms.json"

# Load configuration from JSON or create initial setup
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            # Handle both old format (direct dict) and new format (with "vms" key)
            if "vms" in data:
                vms_data = data["vms"]
            else:
                vms_data = data
            
            # Ensure all VMs have required fields
            for vm_name, vm_info in vms_data.items():
                if "color" not in vm_info:
                    vm_info["color"] = "CYAN"
                if "users" not in vm_info:
                    vm_info["users"] = vm_info.get("usuarios", [])
                # Remove old "usuarios" field if present
                if "usuarios" in vm_info:
                    vm_info.pop("usuarios")
            
            return vms_data
    else:
        return {
            "VM1": {
                "ip": "your.vm.ip",  # Replace with actual IP
                "users": ["root", "your_user1"],
                "color": "RED"
            }
        }

# Save configuration
def save_config(vms):
    with open(CONFIG_FILE, "w") as f:
        json.dump(vms, f, indent=4)

# Color name mapping
COLORS = {
    "RED": RED,
    "GREEN": GREEN,
    "CYAN": CYAN,
    "YELLOW": YELLOW
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

vms = load_config()

def ssh_menu():
    while True:
        clear_screen()
        print(f"{CYAN}╔════════════════════════════════╗{RESET}")
        print(f"{CYAN}║         SSH MANAGER            ║{RESET}")
        print(f"{CYAN}╚════════════════════════════════╝{RESET}\n")

        print("0. Exit")
        for idx, (vm_name, vm_info) in enumerate(vms.items(), start=1):
            color = COLORS.get(vm_info.get("color", "CYAN"), RESET)
            print(f"{idx}. {color}{vm_name}{RESET} ({vm_info['ip']})")
        print(f"{len(vms)+1}. Admin Menu\n")

        vm_option = input(f"{CYAN}Select an option:{RESET} ")

        if not vm_option.isdigit():
            continue

        vm_option = int(vm_option)
        if vm_option == 0:
            save_config(vms)
            clear_screen()
            print(f"{CYAN}Goodbye!{RESET}")
            sys.exit(0)
        elif vm_option == len(vms)+1:
            admin_menu()
            continue
        elif vm_option < 1 or vm_option > len(vms):
            continue

        vm_name = list(vms.keys())[vm_option - 1]
        connect_user_menu(vm_name)

def connect_user_menu(vm_name):
    """User submenu for connection"""
    vm_info = vms[vm_name]
    ip = vm_info["ip"]
    color = COLORS.get(vm_info.get("color", "CYAN"), RESET)

    while True:
        clear_screen()
        print(f"{color}=== Users for {vm_name} ({ip}) ==={RESET}\n")
        print("0. Back")
        for idx, user in enumerate(vm_info["users"], start=1):
            print(f"{idx}. {user}")

        user_option = input(f"\n{CYAN}Select user:{RESET} ")

        if not user_option.isdigit():
            continue

        user_option = int(user_option)
        if user_option == 0:
            return
        elif 1 <= user_option <= len(vm_info["users"]):
            username = vm_info["users"][user_option-1]
            clear_screen()
            print(f"{color}Opening SSH to {vm_name} ({ip}) as {username}...{RESET}\n")
            os.system(f'start cmd /k ssh {username}@{ip}')
        # Returns automatically to menu after closing connection

def admin_menu():
    """VM administration menu"""
    while True:
        clear_screen()
        print(f"{YELLOW}=== ADMIN MENU ==={RESET}\n")
        print("0. Back")
        for idx, vm_name in enumerate(vms.keys(), start=1):
            print(f"{idx}. {vm_name}")
        print(f"{len(vms)+1}. Add new VM")
        print(f"{len(vms)+2}. Delete VM\n")

        option = input(f"{CYAN}Select option:{RESET} ")

        if not option.isdigit():
            continue

        option = int(option)
        if option == 0:
            return
        elif option == len(vms)+1:
            add_vm()
        elif option == len(vms)+2:
            delete_vm()
        elif 1 <= option <= len(vms):
            vm_name = list(vms.keys())[option-1]
            edit_vm(vm_name)

def edit_vm(vm_name):
    """Edit IP and users of a VM"""
    vm_info = vms[vm_name]
    while True:
        clear_screen()
        print(f"{YELLOW}Editing {vm_name}{RESET}")
        print(f"IP: {vm_info['ip']}")
        print(f"Users: {', '.join(vm_info['users'])}\n")
        print("0. Back")
        print("1. Change IP")
        print("2. Add user")
        print("3. Remove user\n")

        option = input(f"{CYAN}Select option:{RESET} ")

        if option == "0":
            return
        elif option == "1":
            new_ip = input("New IP: ")
            vm_info["ip"] = new_ip
        elif option == "2":
            new_user = input("New user: ")
            if new_user not in vm_info["users"]:
                vm_info["users"].append(new_user)
        elif option == "3":
            for idx, user in enumerate(vm_info["users"], start=1):
                print(f"{idx}. {user}")
            delete_user = input("Select user to remove: ")
            if delete_user.isdigit() and 1 <= int(delete_user) <= len(vm_info["users"]):
                confirm = input(f"Are you sure? (y/n): ").lower()
                if confirm == "y":
                    vm_info["users"].pop(int(delete_user)-1)
        save_config(vms)

def add_vm():
    clear_screen()
    name = input("New VM name: ")
    ip = input("VM IP: ")
    color = input("Color (RED/GREEN/CYAN/YELLOW): ").upper()
    vms[name] = {"ip": ip, "users": [], "color": color if color in COLORS else "CYAN"}
    save_config(vms)

def delete_vm():
    clear_screen()
    print(f"{RED}=== DELETE VM ==={RESET}\n")
    print("0. Back")
    for idx, vm_name in enumerate(vms.keys(), start=1):
        print(f"{idx}. {vm_name}")
    option = input("Select VM to delete: ")
    if not option.isdigit():
        return
    option = int(option)
    if option == 0 or option > len(vms):
        return
    vm_name = list(vms.keys())[option-1]
    confirm = input(f"Are you sure you want to delete {vm_name}? (y/n): ").lower()
    if confirm == "y":
        vms.pop(vm_name)
        save_config(vms)

# Start the menu
ssh_menu()
