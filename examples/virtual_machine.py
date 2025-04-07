from kubernetes import config
from ocp_resources.virtual_machine import VirtualMachine

config.load_kube_config()

# Define a VM
vm = VirtualMachine(
    name="vm-example",
    namespace="namespace-example",
    body={
        "spec": {
            "runStrategy": "Halted",
            "template": {
                "spec": {
                    "domain": {
                        "devices": {"disks": [{"name": "disk0", "disk": {"bus": "virtio"}}]},
                        "resources": {"requests": {"memory": "64Mi"}},
                    },
                    "volumes": [
                        {
                            "name": "disk0",
                            "containerDisk": {"image": "kubevirt/cirros-container-disk-demo"},
                        }
                    ],
                },
            },
        }
    },
)

# VM operations
vm.create()
vm.start()
vm.vmi.wait_until_running(timeout=180)
vm.stop()
