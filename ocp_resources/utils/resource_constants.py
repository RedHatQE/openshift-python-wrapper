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
        SCHEDULING_DISABLED: str = "Ready,SchedulingDisabled"
        CRASH_LOOPBACK_OFF: str = "CrashLoopBackOff"
        IMAGE_PULL_BACK_OFF: str = "ImagePullBackOff"
        ERR_IMAGE_PULL: str = "ErrImagePull"
        ACTIVE: str = "Active"
        ESTABLISHED: str = "Established"

    class Condition:
        UPGRADEABLE: str = "Upgradeable"
        AVAILABLE: str = "Available"
        DEGRADED: str = "Degraded"
        PROGRESSING: str = "Progressing"
        CREATED: str = "Created"
        RECONCILE_COMPLETE: str = "ReconcileComplete"
        READY: str = "Ready"
        FAILING: str = "Failing"
        NETWORK_READY: str = "NetworkReady"
        ARCHIVED: str = "Archived"
        CANCELED: str = "Canceled"

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
            SUCCEEDED: str = "Succeeded"

    class Type:
        CLUSTER_IP: str = "ClusterIP"
        NODE_PORT: str = "NodePort"
        LOAD_BALANCER: str = "LoadBalancer"

    class Interface:
        class State:
            UP: str = "up"
            DOWN: str = "down"
            ABSENT: str = "absent"

    class ProviderType:
        VSPHERE: str = "vsphere"
        OPENSHIFT: str = "openshift"
        RHV: str = "ovirt"
        OVA: str = "ova"
        OPENSTACK: str = "openstack"

    class Backup:
        class Status:
            NEW: str = "New"
            FAILEDVALIDATION: str = "FailedValidation"
            INPROGRESS: str = "InProgress"
            WAITINGFORPLUGINOPERATIONS: str = "WaitingForPluginOperations"
            WAITINGFORPLUGINOPERATIONSPARTIALLYFAILED: str = "WaitingForPluginOperationsPartiallyFailed"
            FINALIZING: str = "Finalizing"
            FINALIZINGPARTIALLYFAILED: str = "FinalizingPartiallyFailed"
            COMPLETED: str = "Completed"
            PARTIALLYFAILED: str = "PartiallyFailed"
            FAILED: str = "Failed"
            DELETING: str = "Deleting"
