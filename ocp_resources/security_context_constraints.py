from ocp_resources.resource import Resource


class SecurityContextConstraints(Resource):
    api_group = Resource.ApiGroup.SECURITY_OPENSHIFT_IO

    def __init__(
        self,
        allow_host_dir_volume_plugin=False,
        allow_host_ipc=False,
        allow_host_network=False,
        allow_host_pid=False,
        allow_host_ports=False,
        allow_privilege_escalation=None,
        allow_privileged_container=False,
        allowed_capabilities=None,
        allowed_flex_volumes=None,
        allowed_unsafe_sysctls=None,
        default_add_capabilities=None,
        default_allow_privilege_escalation=None,
        forbidden_sysctls=None,
        fs_group=None,
        groups=None,
        priority=0,
        read_only_root_filesystem=False,
        required_drop_capabilities=None,
        run_as_user=None,
        se_linux_context=None,
        seccomp_profiles=None,
        supplemental_groups=None,
        users=None,
        volumes=None,
        **kwargs,
    ):
        """
        Security Context Constraints object. API reference:
        https://docs.openshift.com/container-platform/4.13/rest_api/security_apis/securitycontextconstraints-security-openshift-io-v1.html

        Args:
            allow_host_dir_volume_plugin (bool): Determines if the policy allow containers to use the HostDir volume
                plugin
            allow_host_ipc (bool): Determines if the policy allows host ipc in the containers.
            allow_host_network (bool): Determines if the policy allows the use of HostNetwork in the pod spec.
            allow_host_pid (bool): Determines if the policy allows host pid in the containers.
            allow_host_ports (bool): Determines if the policy allows host ports in the containers.
            allow_privilege_escalation (bool): Determines if a pod can request to allow privilege escalation.
            allow_privileged_container (bool): Determines if a container can request to be run as privileged.
            allowed_capabilities (list): List of capabilities that can be requested to add to the container. To allow
                all capabilities you may use '*'.
            allowed_flex_volumes (list): Allowed Flexvolumes. Empty or nil indicates that all Flexvolumes may be used.
                This parameter is effective only when the usage of the Flexvolumes is allowed in the "Volumes" field.
            allowed_unsafe_sysctls (list): Explicitly allowed unsafe sysctls.
            default_add_capabilities (list):Default set of capabilities that will be added to the container
            default_allow_privilege_escalation (bool): Controls the default setting for whether a process can gain more
                privileges than its parent process.
            forbidden_sysctls (list): Explicitly forbidden sysctls. Single * means all sysctls are forbidden.
            fs_group (str): The strategy that will dictate what fs group is used by the SecurityContext.
            groups (list): The groups that have permission to use this security context constraints
            priority (int): Influences the sort order of SCCs when evaluating which SCCs to try first for a given pod
                request.
            read_only_root_filesystem (bool): Whether toorce containers to run with a read only root file system.
            required_drop_capabilities (list): The capabilities that will be dropped from the container.
            run_as_user (dict): The strategy that will dictate what RunAsUser is used in the SecurityContext.
            se_linux_context (dict): The strategy that will dictate what labels will be set in the SecurityContext.
            seccomp_profiles (list): The allowed profiles that may be set for the pod or container’s seccomp
                annotations.
            supplemental_groups (dict): The strategy that will dictate what supplemental groups are used by the
                SecurityContext.
            users (list) : The users who have permissions to use this security context constraints.
            volumes (list):White list of allowed volume plugins. To allow all volumes you may use "*".
        """

        super().__init__(**kwargs)
        self.allow_host_dir_volume_plugin = allow_host_dir_volume_plugin
        self.allow_host_ipc = allow_host_ipc
        self.allow_host_network = allow_host_network
        self.allow_host_pid = allow_host_pid
        self.allow_host_ports = allow_host_ports
        self.allow_privilege_escalation = allow_privilege_escalation
        self.allow_privileged_container = allow_privileged_container
        self.allowed_capabilities = allowed_capabilities
        self.allowed_flex_volumes = allowed_flex_volumes
        self.allowed_unsafe_sysctls = allowed_unsafe_sysctls
        self.default_add_capabilities = default_add_capabilities
        self.default_allow_privilege_escalation = default_allow_privilege_escalation
        self.forbidden_sysctls = forbidden_sysctls
        self.fs_group = fs_group
        self.groups = groups
        self.priority = priority
        self.read_only_root_filesystem = read_only_root_filesystem
        self.required_drop_capabilities = required_drop_capabilities
        self.run_as_user = run_as_user
        self.se_linux_context = se_linux_context
        self.seccomp_profiles = seccomp_profiles
        self.supplemental_groups = supplemental_groups
        self.users = users
        self.volumes = volumes

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update()
            if self.allow_host_dir_volume_plugin:
                self.res["allowHostDirVolumePlugin"] = self.allow_host_dir_volume_plugin

            if self.allow_host_ipc:
                self.res["allowHostIPC"] = self.allow_host_ipc

            if self.allow_host_network:
                self.res["allowHostNetwork"] = self.allow_host_network

            if self.allow_host_pid:
                self.res["allowHostPID"] = self.allow_host_pid

            if self.allow_host_ports:
                self.res["allowHostPorts"] = self.allow_host_ports

            if self.allow_privilege_escalation:
                self.res["allowPrivilegeEscalation"] = self.allow_privilege_escalation

            if self.allow_privileged_container:
                self.res["allowPrivilegedContainer"] = self.allow_privileged_container

            if self.allowed_capabilities:
                self.res["allowedCapabilities"] = self.allowed_capabilities

            if self.allowed_flex_volumes:
                self.res["allowedFlexVolumes"] = self.allowed_flex_volumes

            if self.allowed_unsafe_sysctls:
                self.res["allowedUnsafeSysctls"] = self.allowed_unsafe_sysctls

            if self.default_add_capabilities:
                self.res["defaultAddCapabilities"] = self.default_add_capabilities

            if self.default_allow_privilege_escalation:
                self.res[
                    "defaultAllowPrivilegeEscalation"
                ] = self.default_allow_privilege_escalation

            if self.forbidden_sysctls:
                self.res["forbiddenSysctls"] = self.forbidden_sysctls

            if self.fs_group:
                self.res["fsGroup"] = self.fs_group

            if self.groups:
                self.res["groups"] = self.groups

            if self.priority:
                self.res["priority"] = self.priority

            if self.read_only_root_filesystem:
                self.res["readOnlyRootFilesystem"] = self.read_only_root_filesystem

            if self.required_drop_capabilities:
                self.res["requiredDropCapabilities"] = self.required_drop_capabilities

            if self.run_as_user:
                self.res["runAsUser"] = self.run_as_user

            if self.se_linux_context:
                self.res["seLinuxContext"] = self.se_linux_context

            if self.seccomp_profiles:
                self.res["seccompProfiles"] = self.seccomp_profiles

            if self.supplemental_groups:
                self.res["supplementalGroups"] = self.supplemental_groups

            if self.users:
                self.res["users"] = self.users

            if self.volumes:
                self.res["volumes"] = self.volumes
