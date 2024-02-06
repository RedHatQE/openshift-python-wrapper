from ocp_resources.virtual_machine import VirtualMachine

# Create a VM
with VirtualMachine(
    name="vm-example",
    namespace="namespace-example",
    node_selector="worker-node-example",
) as vm:
    vm.start()

# VM operations
vm.stop()
vm.restart()

# Get VM VMI
test_vmi = vm.vmi

# After having a VMI, we can wait until VMI is in running state:
test_vmi.wait_until_running()

# Then, we can get the virt launcher Pod and execute a command on it:
command_output = test_vmi.virt_launcher_pod.execute(command="command-example")
