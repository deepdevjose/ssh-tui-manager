import os

# Set up the virtual machines and their users
vms = {
    "VM1": {
        "ip": "your.debian.vm.ip",  # Replace with actual IP
        "usuarios": ["root", "your_user1"],
    },
}

while True:
    # Show SSH menu
    print("\n=== SSH Menu ===")
    for idx, vm_name in enumerate(vms.keys(), start=1):
        print(f"{idx}. {vm_name}")
    print(f"{len(vms)+1}. Exit")

    # Choose VM
    opcion_vm = input("Select the VM number: ")

    if not opcion_vm.isdigit():
        print("Invalid option, please enter a number.")
        continue

    opcion_vm = int(opcion_vm)
    if opcion_vm == len(vms) + 1:
        print("Exiting SSH menu. Goodbye!")
        break
    elif opcion_vm < 1 or opcion_vm > len(vms):
        print("Invalid option, try again.")
        continue

    vm_name = list(vms.keys())[opcion_vm - 1]
    ip = vms[vm_name]["ip"]

    # Show users for the selected VM
    usuarios = vms[vm_name]["usuarios"]
    print(f"\n=== Users for {vm_name} ===")
    for idx, user in enumerate(usuarios, start=1):
        print(f"{idx}. {user}")

    opcion_user = input("Select the user number: ")

    if not opcion_user.isdigit() or int(opcion_user) < 1 or int(opcion_user) > len(usuarios):
        print("Invalid user, try again.")
        continue

    usuario = usuarios[int(opcion_user) - 1]

    # Open SSH connection in a new CMD window
    print(f"\nOpening SSH to {vm_name} ({ip}) as {usuario} in a new window...\n")
    os.system(f'start cmd /k ssh {usuario}@{ip}')
