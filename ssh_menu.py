import os
import sys
import json
import msvcrt  # For Windows keyboard input

# ANSI Colors
RED = "\033[38;5;196m"        # Bright red
GREEN = "\033[38;5;46m"       # Bright green  
CYAN = "\033[38;5;51m"        # Bright cyan
YELLOW = "\033[38;5;226m"     # Bright yellow
BLUE = "\033[38;5;39m"        # Bright blue
MAGENTA = "\033[38;5;201m"    # Bright magenta
WHITE = "\033[38;5;15m"       # Bright white
GRAY = "\033[38;5;244m"       # Gray
ORANGE = "\033[38;5;208m"     # Orange
PURPLE = "\033[38;5;141m"     # Purple
RESET = "\033[0m"
HIGHLIGHT = "\033[48;5;24m\033[38;5;15m"  # Blue background with white text
BORDER = "\033[38;5;39m"      # Blue for borders

CONFIG_FILE = "vms.json"

# Load configuration from JSON or create initial setup
def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Handle both old format (direct dict) and new format (with "vms" key)
                if "vms" in data:
                    vms_data = data["vms"]
                else:
                    vms_data = data
                
                # Validate that vms_data is a dictionary
                if not isinstance(vms_data, dict):
                    print(f"{YELLOW}⚠ Warning: Invalid configuration format in {CONFIG_FILE}. Using defaults.{RESET}")
                    return get_default_config()
                
                # Ensure all VMs have required fields
                for vm_name, vm_info in vms_data.items():
                    if not isinstance(vm_info, dict):
                        print(f"{YELLOW}⚠ Warning: Invalid VM configuration for '{vm_name}'. Skipping.{RESET}")
                        continue
                    if "color" not in vm_info:
                        vm_info["color"] = "CYAN"
                    if "users" not in vm_info:
                        vm_info["users"] = vm_info.get("usuarios", [])
                    if "ip" not in vm_info:
                        vm_info["ip"] = "127.0.0.1"  # Default fallback IP
                    # Ensure users is a list
                    if not isinstance(vm_info["users"], list):
                        vm_info["users"] = []
                    # Remove old "usuarios" field if present
                    if "usuarios" in vm_info:
                        vm_info.pop("usuarios")
                
                return vms_data
        else:
            # File doesn't exist, create with default configuration
            print(f"{CYAN}ℹ Configuration file '{CONFIG_FILE}' not found. Creating with default settings.{RESET}")
            return get_default_config()
    except json.JSONDecodeError as e:
        print(f"{RED}✗ Error: Invalid JSON in {CONFIG_FILE}. Line {e.lineno}: {e.msg}{RESET}")
        print(f"{YELLOW}ℹ Using default configuration. Your original file will be backed up.{RESET}")
        
        # Backup corrupted file
        backup_file = f"{CONFIG_FILE}.backup"
        try:
            import shutil
            shutil.copy2(CONFIG_FILE, backup_file)
            print(f"{CYAN}ℹ Corrupted file backed up as '{backup_file}'{RESET}")
        except Exception:
            pass
        
        return get_default_config()
    except PermissionError:
        print(f"{RED}✗ Error: Permission denied accessing {CONFIG_FILE}{RESET}")
        print(f"{YELLOW}ℹ Using default configuration (changes won't be saved){RESET}")
        return get_default_config()
    except Exception as e:
        print(f"{RED}✗ Error loading configuration: {str(e)}{RESET}")
        print(f"{YELLOW}ℹ Using default configuration{RESET}")
        return get_default_config()

def get_default_config():
    """Return default VM configuration"""
    return {
        "Production Server": {
            "ip": "192.168.1.100",  # Default production-like IP
            "users": ["root", "admin", "deploy"],
            "color": "BLUE"
        },
        "Development Server": {
            "ip": "192.168.1.101",  # Default dev-like IP
            "users": ["dev", "root"],
            "color": "GREEN"
        }
    }

# Save configuration
def save_config(vms):
    """Save VMs configuration to JSON file with error handling"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(vms, f, indent=4, ensure_ascii=False)
        return True
    except PermissionError:
        print(f"{RED}✗ Error: Permission denied writing to {CONFIG_FILE}{RESET}")
        print(f"{YELLOW}ℹ Changes cannot be saved. Check file permissions.{RESET}")
        return False
    except OSError as e:
        print(f"{RED}✗ Error: Cannot write to {CONFIG_FILE}. {str(e)}{RESET}")
        print(f"{YELLOW}ℹ Changes cannot be saved.{RESET}")
        return False
    except Exception as e:
        print(f"{RED}✗ Unexpected error saving configuration: {str(e)}{RESET}")
        return False

# Color name mapping
COLORS = {
    "RED": RED,
    "GREEN": GREEN,
    "CYAN": CYAN,
    "YELLOW": YELLOW,
    "BLUE": BLUE,
    "MAGENTA": MAGENTA,
    "WHITE": WHITE,
    "ORANGE": ORANGE,
    "PURPLE": PURPLE
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key():
    """Get a single key press on Windows"""
    if os.name == 'nt':  # Windows
        key = msvcrt.getch()
        if key == b'\xe0' or key == b'\x00':  # Special key (arrow keys)
            key = msvcrt.getch()
            if key == b'H':  # Up arrow
                return 'UP'
            elif key == b'P':  # Down arrow
                return 'DOWN'
            elif key == b'M':  # Right arrow
                return 'RIGHT'
            elif key == b'K':  # Left arrow
                return 'LEFT'
        elif key == b'\r':  # Enter
            return 'ENTER'
        elif key == b'\x1b':  # Escape
            return 'ESC'
        elif key.isdigit():  # Number keys
            return key.decode('utf-8')
        else:
            return key.decode('utf-8', errors='ignore')
    return None

def arrow_menu(options, title="Select an option"):
    """Display a menu with arrow key navigation"""
    selected = 0
    while True:
        clear_screen()
        print(f"{BLUE}{title}{RESET}\n")
        
        for i, option in enumerate(options):
            if i == selected:
                print(f"{HIGHLIGHT} ➤ {option} {RESET}")
            else:
                print(f"{GRAY}   {option}{RESET}")
        
        print(f"\n{CYAN}┌─ Controls ────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{WHITE} ↑↓{GRAY} Navigate  {WHITE}Enter/→{GRAY} Select  {WHITE}←/Esc{GRAY} Back  {WHITE}0-9{GRAY} Direct {CYAN}│{RESET}")
        print(f"{CYAN}└───────────────────────────────────────────────────┘{RESET}")
        
        key = get_key()
        
        if key == 'UP':
            selected = (selected - 1) % len(options)
        elif key == 'DOWN':
            selected = (selected + 1) % len(options)
        elif key == 'ENTER' or key == 'RIGHT':  # Enter or Right arrow to select
            return selected
        elif key == 'ESC' or key == 'LEFT':  # Escape or Left arrow to go back
            return -1  # Go back
        elif key and key.isdigit():
            num = int(key)
            if 0 <= num < len(options):
                return num

vms = load_config()

def ssh_menu():
    while True:
        # Create menu options
        options = ["Exit"]
        vm_names = list(vms.keys())
        
        for vm_name in vm_names:
            vm_info = vms[vm_name]
            color = COLORS.get(vm_info.get("color", "CYAN"), RESET)
            options.append(f"{color}{vm_name}{RESET} ({vm_info['ip']})")
        
        options.append("Admin Menu")
        
        # Show menu with arrow navigation
        clear_screen()
        print(f"{BORDER}╔══════════════════════════════════════════════╗{RESET}")
        print(f"{BORDER}║{CYAN}              SSH MANAGER v2.1              {BORDER}║{RESET}")
        print(f"{BORDER}╠══════════════════════════════════════════════╣{RESET}")
        print(f"{BORDER}║{GRAY}         Professional Terminal Access        {BORDER}║{RESET}")
        print(f"{BORDER}╚══════════════════════════════════════════════╝{RESET}\n")
        
        selection = arrow_menu(options, "Select an option:")
        
        if selection == -1:  # ESC or Left arrow pressed
            continue
        elif selection == 0:  # Exit
            save_config(vms)
            clear_screen()
            print(f"{BLUE}╔══════════════════════════════════════════════╗{RESET}")
            print(f"{BLUE}║{WHITE}              GOODBYE!                       {BLUE}║{RESET}")
            print(f"{BLUE}║{GRAY}         Thanks for using SSH Manager        {BLUE}║{RESET}")
            print(f"{BLUE}╚══════════════════════════════════════════════╝{RESET}")
            print(f"\n{CYAN}Configuration saved. Session terminated.{RESET}")
            sys.exit(0)
        elif selection == len(options) - 1:  # Admin Menu
            admin_menu()
        elif 1 <= selection <= len(vm_names):  # VM selected
            vm_name = vm_names[selection - 1]
            vm_info = vms[vm_name]
            
            # Quick connect feature: if VM has only one user, connect directly
            if len(vm_info["users"]) == 1:
                username = vm_info["users"][0]
                color = COLORS.get(vm_info.get("color", "CYAN"), RESET)
                clear_screen()
                print(f"{BLUE}╔══════════════════════════════════════════════╗{RESET}")
                print(f"{BLUE}║{WHITE}              QUICK CONNECT                  {BLUE}║{RESET}")
                print(f"{BLUE}╚══════════════════════════════════════════════╝{RESET}\n")
                
                print(f"{CYAN}Target:{RESET} {color}{vm_name}{RESET} ({WHITE}{vm_info['ip']}{RESET})")
                print(f"{CYAN}User:{RESET} {YELLOW}{username}{RESET}")
                print(f"{CYAN}Status:{RESET} {GREEN}Ready to connect{RESET}\n")
                
                print(f"{CYAN}┌─ Quick Actions ──────────────────────────────────┐{RESET}")
                print(f"{CYAN}│{WHITE} Enter/→{GRAY} Connect Now   {WHITE}Any Key{GRAY} Open User Menu     {CYAN}│{RESET}")
                print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}")
                
                key = get_key()
                if key == 'ENTER' or key == 'RIGHT':
                    clear_screen()
                    print(f"{BLUE}╔══════════════════════════════════════════════╗{RESET}")
                    print(f"{BLUE}║{WHITE}              SSH CONNECTION                 {BLUE}║{RESET}")
                    print(f"{BLUE}╚══════════════════════════════════════════════╝{RESET}\n")
                    
                    print(f"{CYAN}➤ Target:{RESET} {color}{vm_name}{RESET} ({WHITE}{vm_info['ip']}{RESET})")
                    print(f"{CYAN}➤ User:{RESET} {YELLOW}{username}{RESET}")
                    print(f"{CYAN}➤ Status:{RESET} {GREEN}Launching SSH session...{RESET}\n")
                    
                    os.system(f'start cmd /k ssh {username}@{vm_info["ip"]}')
                    input(f"{GRAY}Press Enter to return to menu...{RESET}")
                else:
                    connect_user_menu(vm_name)
            else:
                connect_user_menu(vm_name)

def connect_user_menu(vm_name):
    """User submenu for connection and user management"""
    vm_info = vms[vm_name]
    ip = vm_info["ip"]
    color = COLORS.get(vm_info.get("color", "CYAN"), RESET)

    while True:
        # Create menu options
        options = ["Back"]
        
        for user in vm_info["users"]:
            options.append(f"Connect as {user}")
        
        options.append("Add new user")
        options.append("Remove user")
        
        # Show menu with arrow navigation
        selection = arrow_menu(options, f"{color}=== Users for {vm_name} ({ip}) ==={RESET}")
        
        if selection == -1 or selection == 0:  # ESC/Left arrow or Back
            return
        elif 1 <= selection <= len(vm_info["users"]):  # Connect as user
            username = vm_info["users"][selection - 1]
            clear_screen()
            print(f"{BLUE}╔══════════════════════════════════════════════╗{RESET}")
            print(f"{BLUE}║{WHITE}              SSH CONNECTION                 {BLUE}║{RESET}")
            print(f"{BLUE}╚══════════════════════════════════════════════╝{RESET}\n")
            
            print(f"{CYAN}➤ Target:{RESET} {color}{vm_name}{RESET} ({WHITE}{ip}{RESET})")
            print(f"{CYAN}➤ User:{RESET} {YELLOW}{username}{RESET}")
            print(f"{CYAN}➤ Status:{RESET} {GREEN}Launching SSH session...{RESET}\n")
            
            os.system(f'start cmd /k ssh {username}@{ip}')
            input(f"{GRAY}Press Enter to return to menu...{RESET}")
        elif selection == len(vm_info["users"]) + 1:  # Add new user
            clear_screen()
            print(f"{BLUE}╔══════════════════════════════════════════════╗{RESET}")
            print(f"{BLUE}║{WHITE}              ADD USER                       {BLUE}║{RESET}")
            print(f"{BLUE}╚══════════════════════════════════════════════╝{RESET}\n")
            
            print(f"{CYAN}Target VM:{RESET} {color}{vm_name}{RESET}")
            print(f"{GRAY}ℹ Type 'cancel' or 'exit' to abort{RESET}\n")
            
            while True:
                new_user = input(f"{CYAN}Username: {WHITE}").strip()
                print(f"{RESET}", end="")
                
                if new_user.lower() in ['cancel', 'exit', 'quit']:
                    print(f"\n{YELLOW}ℹ User creation cancelled.{RESET}")
                    break
                elif not new_user:
                    print(f"{RED}✗ Username cannot be empty!{RESET}")
                    continue
                elif new_user in vm_info["users"]:
                    print(f"{RED}✗ User '{new_user}' already exists!{RESET}")
                    continue
                elif len(new_user) < 2:
                    print(f"{RED}✗ Username must be at least 2 characters long!{RESET}")
                    continue
                elif any(char in new_user for char in [' ', '@', '#', '$', '%', '^', '&', '*']):
                    print(f"{RED}✗ Username contains invalid characters!{RESET}")
                    print(f"{GRAY}Use only letters, numbers, underscore, and hyphen{RESET}")
                    continue
                else:
                    vm_info["users"].append(new_user)
                    if save_config(vms):
                        print(f"\n{GREEN}✓ User {YELLOW}{new_user}{GREEN} added successfully!{RESET}")
                    else:
                        print(f"\n{YELLOW}⚠ User {new_user} added but configuration could not be saved.{RESET}")
                    break
            
            input(f"\n{GRAY}Press Enter to return...{RESET}")
        elif selection == len(vm_info["users"]) + 2:  # Remove user
            if not vm_info["users"]:
                clear_screen()
                print(f"{RED}╔══════════════════════════════════════════════╗{RESET}")
                print(f"{RED}║{WHITE}              NO USERS                       {RED}║{RESET}")
                print(f"{RED}╚══════════════════════════════════════════════╝{RESET}\n")
                
                print(f"{CYAN}VM:{RESET} {color}{vm_name}{RESET}")
                print(f"{RED}✗ No users available to remove.{RESET}")
                print(f"{CYAN}ℹ Add users first before attempting to remove them.{RESET}")
                
                input(f"\n{GRAY}Press Enter to return...{RESET}")
            else:
                # Create submenu for user removal
                remove_options = ["Cancel"]
                for user in vm_info["users"]:
                    remove_options.append(f"Remove {user}")
                
                remove_selection = arrow_menu(remove_options, f"{RED}=== Remove User from {vm_name} ==={RESET}")
                
                if remove_selection > 0:  # User selected for removal
                    user_to_remove = vm_info["users"][remove_selection - 1]
                    clear_screen()
                    print(f"{RED}╔══════════════════════════════════════════════╗{RESET}")
                    print(f"{RED}║{WHITE}              REMOVE USER                    {RED}║{RESET}")
                    print(f"{RED}╚══════════════════════════════════════════════╝{RESET}\n")
                    
                    print(f"{CYAN}VM:{RESET} {color}{vm_name}{RESET}")
                    print(f"{CYAN}User to Remove:{RESET} {YELLOW}{user_to_remove}{RESET}\n")
                    print(f"{RED}⚠ This will remove the user from this VM.{RESET}\n")
                    
                    confirm = input(f"{CYAN}Type 'yes' to confirm removal: {WHITE}")
                    print(f"{RESET}", end="")
                    
                    if confirm.lower() == "yes":
                        vm_info["users"].remove(user_to_remove)
                        if save_config(vms):
                            print(f"\n{GREEN}✓ User {user_to_remove} removed successfully!{RESET}")
                        else:
                            print(f"\n{YELLOW}⚠ User {user_to_remove} removed but configuration could not be saved.{RESET}")
                    else:
                        print(f"\n{YELLOW}ℹ Removal cancelled.{RESET}")
                    
                    input(f"\n{GRAY}Press Enter to return...{RESET}")

def admin_menu():
    """VM administration menu"""
    while True:
        # Create menu options
        options = ["Back"]
        vm_names = list(vms.keys())
        
        for vm_name in vm_names:
            options.append(f"Edit {vm_name}")
        
        options.append("Add new VM")
        options.append("Delete VM")
        
        # Show menu with arrow navigation
        selection = arrow_menu(options, f"{YELLOW}=== ADMIN MENU ==={RESET}")
        
        if selection == -1 or selection == 0:  # ESC/Left arrow or Back
            return
        elif selection == len(options) - 2:  # Add new VM
            add_vm()
        elif selection == len(options) - 1:  # Delete VM
            delete_vm()
        elif 1 <= selection <= len(vm_names):  # Edit VM
            vm_name = vm_names[selection - 1]
            edit_vm(vm_name)

def edit_vm(vm_name):
    """Edit VM IP address"""
    vm_info = vms[vm_name]
    clear_screen()
    print(f"{BLUE}╔══════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║{WHITE}              EDIT VM                        {BLUE}║{RESET}")
    print(f"{BLUE}╚══════════════════════════════════════════════╝{RESET}\n")
    
    color = COLORS.get(vm_info.get("color", "CYAN"), RESET)
    print(f"{CYAN}VM Name:{RESET} {color}{vm_name}{RESET}")
    print(f"{CYAN}Current IP:{RESET} {WHITE}{vm_info['ip']}{RESET}")
    print(f"{CYAN}Users:{RESET} {YELLOW}{', '.join(vm_info['users']) if vm_info['users'] else 'None'}{RESET}\n")
    
    while True:
        new_ip = input(f"{CYAN}New IP Address (leave blank to keep current): {WHITE}").strip()
        print(f"{RESET}", end="")
        
        if not new_ip:  # Keep current IP
            print(f"\n{YELLOW}ℹ No changes made.{RESET}")
            break
        else:
            # Basic IP format validation
            ip_parts = new_ip.split('.')
            if len(ip_parts) == 4:
                try:
                    valid_ip = all(0 <= int(part) <= 255 for part in ip_parts)
                    if valid_ip:
                        vm_info["ip"] = new_ip
                        if save_config(vms):
                            print(f"\n{GREEN}✓ IP address updated successfully!{RESET}")
                            print(f"{CYAN}Old IP:{RESET} {GRAY}{vm_info.get('old_ip', 'N/A')}{RESET}")
                            print(f"{CYAN}New IP:{RESET} {WHITE}{new_ip}{RESET}")
                        else:
                            print(f"\n{YELLOW}⚠ IP address updated but configuration could not be saved.{RESET}")
                        break
                    else:
                        print(f"{RED}✗ Invalid IP format! Each part must be 0-255{RESET}")
                        print(f"{GRAY}Try again or leave blank to cancel...{RESET}")
                except ValueError:
                    print(f"{RED}✗ Invalid IP format! Use numbers only (e.g., 192.168.1.100){RESET}")
                    print(f"{GRAY}Try again or leave blank to cancel...{RESET}")
            else:
                print(f"{RED}✗ Invalid IP format! Use format: xxx.xxx.xxx.xxx{RESET}")
                print(f"{GRAY}Try again or leave blank to cancel...{RESET}")
    
    input(f"\n{GRAY}Press Enter to return...{RESET}")

def add_vm():
    clear_screen()
    print(f"{BLUE}╔══════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║{WHITE}              ADD NEW VM                     {BLUE}║{RESET}")
    print(f"{BLUE}╚══════════════════════════════════════════════╝{RESET}\n")
    
    print(f"{GRAY}ℹ Type 'cancel' or 'exit' at any time to abort{RESET}\n")
    
    # VM Name validation
    while True:
        name = input(f"{CYAN}VM Name: {WHITE}").strip()
        print(f"{RESET}", end="")
        
        if name.lower() in ['cancel', 'exit', 'quit']:
            print(f"\n{YELLOW}ℹ VM creation cancelled.{RESET}")
            input(f"\n{GRAY}Press Enter to return...{RESET}")
            return
        elif not name:
            print(f"{RED}✗ VM name is required!{RESET}")
            continue
        elif name in vms:
            print(f"{RED}✗ VM name '{name}' already exists!{RESET}")
            continue
        elif len(name) < 2:
            print(f"{RED}✗ VM name must be at least 2 characters long!{RESET}")
            continue
        else:
            print(f"{GREEN}✓ VM name accepted{RESET}")
            break
    
    # IP Address validation
    while True:
        ip = input(f"{CYAN}VM IP Address: {WHITE}").strip()
        print(f"{RESET}", end="")
        
        if ip.lower() in ['cancel', 'exit', 'quit']:
            print(f"\n{YELLOW}ℹ VM creation cancelled.{RESET}")
            input(f"\n{GRAY}Press Enter to return...{RESET}")
            return
        elif not ip:
            print(f"{RED}✗ IP address is required!{RESET}")
            continue
        else:
            # Basic IP format validation
            ip_parts = ip.split('.')
            if len(ip_parts) == 4:
                try:
                    valid_ip = all(0 <= int(part) <= 255 for part in ip_parts)
                    if valid_ip:
                        print(f"{GREEN}✓ IP address accepted{RESET}")
                        break
                    else:
                        print(f"{RED}✗ Invalid IP format! Each part must be 0-255{RESET}")
                except ValueError:
                    print(f"{RED}✗ Invalid IP format! Use numbers only (e.g., 192.168.1.100){RESET}")
            else:
                print(f"{RED}✗ Invalid IP format! Use format: xxx.xxx.xxx.xxx{RESET}")
    
    # Color selection
    print(f"\n{CYAN}Available Colors:{RESET}")
    color_options = ["RED", "GREEN", "CYAN", "YELLOW", "BLUE", "MAGENTA", "WHITE", "ORANGE", "PURPLE"]
    for i, color in enumerate(color_options):
        color_code = COLORS[color]
        print(f"  {i+1}. {color_code}{color}{RESET}")
    
    while True:
        color_choice = input(f"\n{CYAN}Choose color (1-9 or name, default: CYAN): {WHITE}").strip().upper()
        print(f"{RESET}", end="")
        
        if color_choice.lower() in ['cancel', 'exit', 'quit']:
            print(f"\n{YELLOW}ℹ VM creation cancelled.{RESET}")
            input(f"\n{GRAY}Press Enter to return...{RESET}")
            return
        elif not color_choice:  # Default to CYAN
            color = "CYAN"
            print(f"{GREEN}✓ Using default color: {COLORS['CYAN']}CYAN{RESET}")
            break
        elif color_choice.isdigit() and 1 <= int(color_choice) <= len(color_options):
            color = color_options[int(color_choice) - 1]
            print(f"{GREEN}✓ Color selected: {COLORS[color]}{color}{RESET}")
            break
        elif color_choice in COLORS:
            color = color_choice
            print(f"{GREEN}✓ Color selected: {COLORS[color]}{color}{RESET}")
            break
        else:
            print(f"{RED}✗ Invalid color! Choose 1-9 or valid color name{RESET}")
    
    # Final confirmation
    print(f"\n{CYAN}╔══════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{WHITE}              REVIEW NEW VM                  {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════════╝{RESET}")
    print(f"{CYAN}Name:{RESET} {COLORS[color]}{name}{RESET}")
    print(f"{CYAN}IP:{RESET} {WHITE}{ip}{RESET}")
    print(f"{CYAN}Color:{RESET} {COLORS[color]}{color}{RESET}")
    
    while True:
        confirm = input(f"\n{CYAN}Create this VM? (y/n/cancel): {WHITE}").strip().lower()
        print(f"{RESET}", end="")
        
        if confirm in ['cancel', 'exit', 'quit', 'n', 'no']:
            print(f"\n{YELLOW}ℹ VM creation cancelled.{RESET}")
            break
        elif confirm in ['y', 'yes']:
            vms[name] = {"ip": ip, "users": [], "color": color}
            if save_config(vms):
                print(f"\n{GREEN}✓ VM {COLORS[color]}{name}{GREEN} created successfully!{RESET}")
            else:
                print(f"\n{YELLOW}⚠ VM {name} created but configuration could not be saved.{RESET}")
            break
        else:
            print(f"{RED}✗ Please enter 'y' to create, 'n' to cancel, or 'cancel' to abort{RESET}")
    
    input(f"\n{GRAY}Press Enter to return...{RESET}")

def delete_vm():
    if not vms:
        clear_screen()
        print(f"{RED}No VMs to delete.{RESET}")
        input("Press Enter to return...")
        return
    
    # Create menu options
    options = ["Cancel"]
    vm_names = list(vms.keys())
    
    for vm_name in vm_names:
        options.append(f"Delete {vm_name}")
    
    # Show menu with arrow navigation
    selection = arrow_menu(options, f"{RED}=== DELETE VM ==={RESET}")
    
    if selection == -1 or selection == 0:  # ESC/Left arrow or Cancel
        return
    elif 1 <= selection <= len(vm_names):  # VM selected for deletion
        vm_name = vm_names[selection - 1]
        vm_info = vms[vm_name]
        color = COLORS.get(vm_info.get("color", "CYAN"), RESET)
        
        clear_screen()
        print(f"{RED}╔══════════════════════════════════════════════╗{RESET}")
        print(f"{RED}║{WHITE}              CONFIRM DELETION               {RED}║{RESET}")
        print(f"{RED}╚══════════════════════════════════════════════╝{RESET}\n")
        
        print(f"{CYAN}VM to Delete:{RESET} {color}{vm_name}{RESET}")
        print(f"{CYAN}IP Address:{RESET} {WHITE}{vm_info['ip']}{RESET}")
        print(f"{CYAN}Users:{RESET} {YELLOW}{', '.join(vm_info['users']) if vm_info['users'] else 'None'}{RESET}\n")
        
        print(f"{RED}⚠ WARNING: This action cannot be undone!{RESET}\n")
        
        confirm = input(f"{CYAN}Type 'yes' to confirm deletion: {WHITE}")
        print(f"{RESET}", end="")
        
        if confirm.lower() == "yes":
            vms.pop(vm_name)
            if save_config(vms):
                print(f"\n{GREEN}✓ VM {vm_name} deleted successfully!{RESET}")
            else:
                print(f"\n{YELLOW}⚠ VM {vm_name} deleted but configuration could not be saved.{RESET}")
        else:
            print(f"\n{YELLOW}ℹ Deletion cancelled.{RESET}")
        
        input(f"\n{GRAY}Press Enter to return...{RESET}")

# Start the menu
if __name__ == "__main__":
    ssh_menu()
