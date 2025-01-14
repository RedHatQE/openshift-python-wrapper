class ResourceConstants:
    class Status:
        SUCCEEDED: str = "Succeeded"
        FAILED: str = "Failed"
        DELETING: str = "Deleting"
        DEPLOYED: str = "Deployed"
        PENDING: str = "Pending"
        COMPLETED: str = "Completed"
        RUNNING: str = "Running"
        READY: str = "Ready"
        TERMINATING: str = "Terminating"
        ERROR: str = "Error"
        COMPLETE: str = "Complete"
        DEPLOYING: str = "Deploying"
        SCHEDULING_DISABLED = "Ready,SchedulingDisabled"
        CRASH_LOOPBACK_OFF = "CrashLoopBackOff"
        IMAGE_PULL_BACK_OFF = "ImagePullBackOff"
        ERR_IMAGE_PULL = "ErrImagePull"
        ACTIVE = "Active"

    class Condition:
        UPGRADEABLE: str = "Upgradeable"
        AVAILABLE: str = "Available"
        DEGRADED: str = "Degraded"
        PROGRESSING: str = "Progressing"
        CREATED: str = "Created"
        RECONCILE_COMPLETE: str = "ReconcileComplete"
        READY: str = "Ready"
        FAILING: str = "Failing"
        NETWORK_READY = "NetworkReady"

        class Status:
            TRUE: str = "True"
            FALSE: str = "False"
            UNKNOWN: str = "Unknown"

        class Phase:
            INSTALL_READY: str = "InstallReady"
            SUCCEEDED: str = "Succeeded"

        class Reason:
            ALL_REQUIREMENTS_MET: str = "AllRequirementsMet"
            INSTALL_SUCCEEDED: str = "InstallSucceeded"
            NETWORK_ATTACHMENT_DEFINITION_READY: str = "NetworkAttachmentDefinitionReady"
            SYNC_ERROR: str = "SyncError"

        class Type:
            NETWORK_READY: str = "NetworkReady"
            SUCCESSFUL: str = "Successful"
            RUNNING: str = "Running"
            AGENT_CONNECTED: str = "AgentConnected"

    class Type:
        CLUSTER_IP = "ClusterIP"
        NODE_PORT = "NodePort"
        LOAD_BALANCER = "LoadBalancer"

    class Interface:
        class State:
            UP: str = "up"
            DOWN: str = "down"
            ABSENT: str = "absent"

    class ProviderType:
        VSPHERE = "vsphere"
        OPENSHIFT = "openshift"
        RHV = "ovirt"
        OVA = "ova"
