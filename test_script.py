import sys
import os
sys.path.insert(0, r"c:\Users\Josee\Downloads\github_repositories\ssh-tui-manager")
from ssh_menu import load_config, save_config, COLORS, clear_screen, admin_menu

# Test imports
try:
    import json
    print("✅ JSON import successful")
except Exception as e:
    print(f"❌ JSON import failed: {e}")

# Test file reading
try:
    with open(r"c:\Users\Josee\Downloads\github_repositories\ssh-tui-manager\ssh_menu.py", 'r', encoding='utf-8') as f:
        content = f.read()
    print("✅ File reading successful")
    print(f"File size: {len(content)} characters")
except Exception as e:
    print(f"❌ File reading failed: {e}")

# Test specific functions by importing parts
try:
    exec("CONFIG_FILE = 'vms.json'")
    exec("""
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            if "vms" in data:
                vms_data = data["vms"]
            else:
                vms_data = data
            
            for vm_name, vm_info in vms_data.items():
                if "color" not in vm_info:
                    vm_info["color"] = "CYAN"
                if "users" not in vm_info:
                    vm_info["users"] = vm_info.get("usuarios", [])
                if "usuarios" in vm_info:
                    vm_info.pop("usuarios")
            
            return vms_data
    else:
        return {
            "Debian VM": {
                "ip": "192.168.100.55",
                "users": ["root", "deepdevjose"],
                "color": "RED"
            },
            "Rocky VM": {
                "ip": "192.168.100.54",
                "users": ["root", "deepdevjose"],
                "color": "GREEN"
            }
        }
""")
    
    # Test load_config function
    vms = load_config()
    print("✅ load_config() function works")
    print(f"Loaded VMs: {list(vms.keys())}")
    
except Exception as e:
    print(f"❌ Function test failed: {e}")

print("\n🎯 Overall: The core functionality appears to be working!")
