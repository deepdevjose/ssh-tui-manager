import os
import sys
import json

# ANSI escape codes for colored output
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"


CONFIG_FILE = "vms.json"


# Load VM configuration from JSON file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("vms", {})
    else:
        return {
            "VM1": {
                "ip": "your.vm.ip",  # Replace with actual IP
                "users": ["root", "your_user1"],
                "color": "RED"
            }
        }
    
# Save VM configuration
def save_config(vms):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"vms": vms}, f, indent=4)

# Colors for VM display
COLORS = {
    "RED": RED,
    "GREEN": GREEN,
    "CYAN": CYAN,
    "YELLOW": YELLOW
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

vms = load_config()

def connect_menu():
    while True:
        clear_screen()
        print(f"{CYAN}╔════════════════════════════════╗{RESET}")
        print(f"{CYAN}║        SSH MENU - WINDOWS      ║{RESET}")
        print(f"{CYAN}╚════════════════════════════════╝{RESET}\n")

        # Show VMs
        for idx, (vm_name, vm_info) in enumerate(vms.items(), start=1):
            color = COLORS.get(vm_info["color"], RESET)
            print(f" {idx}. {color}{vm_name}{RESET} ({vm_info['ip']})")
        print(f" {len(vms)+1}. {YELLOW}Admin Menu{RESET}")
        print(f" {len(vms)+2}. {YELLOW}Exit{RESET}\n")

        vm_option = input(f"{CYAN}Select an option:{RESET} ")

        if not vm_option.isdigit():
            input(f"{RED}Invalid option, press Enter...{RESET}")
            continue

        vm_option = int(vm_option)
        if vm_option == len(vms) + 2:
            clear_screen()
            print(f"{CYAN}Goodbye!{RESET}")
            save_config(vms)
            sys.exit(0)
        elif vm_option == len(vms) + 1:
            admin_menu()
            continue
        elif vm_option < 1 or vm_option > len(vms):
            input(f"{RED}Invalid option, press Enter...{RESET}")
            continue

        vm_name = list(vms.keys())[vm_option - 1]
        vm_info = vms[vm_name]
        ip = vm_info["ip"]

        # User submenu
        clear_screen()
        color = COLORS.get(vm_info["color"], RESET)
        print(f"{color}=== Users for {vm_name} ==={RESET}\n")
        for idx, user in enumerate(vm_info["users"], start=1):
            print(f" {idx}. {user}")

        user_option = input(f"\n{CYAN}Select the user number:{RESET} ")

        if not user_option.isdigit() or int(user_option) < 1 or int(user_option) > len(vm_info["users"]):
            input(f"{RED}Invalid user, press Enter...{RESET}")
            continue

        username = vm_info["users"][int(user_option) - 1]

        # Open SSH connection in new window
        clear_screen()
        print(f"{color}Opening SSH to {vm_name} ({ip}) as {username}...{RESET}\n")
        os.system(f'start cmd /k ssh {username}@{ip}')

        input(f"{CYAN}\nPress Enter to return to the menu...{RESET}")

def admin_menu():
    while True:
        clear_screen()
        print(f"{YELLOW}=== ADMIN MENU ==={RESET}\n")
        for idx, vm_name in enumerate(vms.keys(), start=1):
            print(f" {idx}. {vm_name}")
        print(f" {len(vms)+1}. Return\n")

        vm_option = input(f"{CYAN}Select VM to edit:{RESET} ")

        if not vm_option.isdigit():
            input(f"{RED}Invalid option, press Enter...{RESET}")
            continue

        vm_option = int(vm_option)
        if vm_option == len(vms) + 1:
            return
        elif vm_option < 1 or vm_option > len(vms):
            input(f"{RED}Invalid VM, press Enter...{RESET}")
            continue

        vm_name = list(vms.keys())[vm_option - 1]
        vm_info = vms[vm_name]

        # Admin submenu
        while True:
            clear_screen()
            print(f"{YELLOW}Editing {vm_name}{RESET}")
            print(f"1. Change IP (current: {vm_info['ip']})")
            print("2. Add user")
            print("3. Remove user")
            print("4. Return\n")

            option = input(f"{CYAN}Select option:{RESET} ")

            if option == "1":
                new_ip = input(f"{CYAN}Enter new IP:{RESET} ")
                vm_info["ip"] = new_ip
                save_config(vms)
                print(f"{GREEN}IP updated!{RESET}")
                input("Press Enter...")

            elif option == "2":
                new_user = input(f"{CYAN}Enter new user:{RESET} ")
                if new_user not in vm_info["users"]:
                    vm_info["users"].append(new_user)
                    save_config(vms)
                    print(f"{GREEN}User added!{RESET}")
                else:
                    print(f"{YELLOW}User already exists.{RESET}")
                input("Press Enter...")

            elif option == "3":
                for idx, user in enumerate(vm_info["users"], start=1):
                    print(f" {idx}. {user}")
                delete_user = input(f"{CYAN}Select user to remove:{RESET} ")
                if delete_user.isdigit() and 1 <= int(delete_user) <= len(vm_info["users"]):
                    removed = vm_info["users"].pop(int(delete_user)-1)
                    save_config(vms)
                    print(f"{GREEN}User {removed} removed!{RESET}")
                else:
                    print(f"{RED}Invalid selection.{RESET}")
                input("Press Enter...")

            elif option == "4":
                break
            else:
                input(f"{RED}Invalid option, press Enter...{RESET}")

# Start main menu
connect_menu()
