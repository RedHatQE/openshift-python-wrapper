# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.resource import MissingRequiredArgumentError, Resource


class SecurityContextConstraints(Resource):
    """
        SecurityContextConstraints governs the ability to make requests that affect the SecurityContext
    that will be applied to a container.
    For historical reasons SCC was exposed under the core Kubernetes API group.
    That exposure is deprecated and will be removed in a future release - users
    should instead use the security.openshift.io group to manage
    SecurityContextConstraints.

    Compatibility level 1: Stable within a major release for a minimum of 12 months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.SECURITY_OPENSHIFT_IO

    def __init__(
        self,
        allow_host_dir_volume_plugin: bool | None = None,
        allow_host_ipc: bool | None = None,
        allow_host_network: bool | None = None,
        allow_host_pid: bool | None = None,
        allow_host_ports: bool | None = None,
        allow_privilege_escalation: Any | None = None,
        allow_privileged_container: bool | None = None,
        allowed_capabilities: Any | None = None,
        allowed_flex_volumes: Any | None = None,
        allowed_unsafe_sysctls: Any | None = None,
        default_add_capabilities: Any | None = None,
        default_allow_privilege_escalation: Any | None = None,
        forbidden_sysctls: Any | None = None,
        fs_group: Any | None = None,
        groups: Any | None = None,
        priority: Any | None = None,
        read_only_root_filesystem: bool | None = None,
        required_drop_capabilities: Any | None = None,
        run_as_user: Any | None = None,
        se_linux_context: Any | None = None,
        seccomp_profiles: Any | None = None,
        supplemental_groups: Any | None = None,
        users: Any | None = None,
        volumes: Any | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            allow_host_dir_volume_plugin (bool): allowHostDirVolumePlugin determines if the policy allow containers to
              use the HostDir volume plugin

            allow_host_ipc (bool): allowHostIPC determines if the policy allows host ipc in the
              containers.

            allow_host_network (bool): allowHostNetwork determines if the policy allows the use of
              HostNetwork in the pod spec.

            allow_host_pid (bool): allowHostPID determines if the policy allows host pid in the
              containers.

            allow_host_ports (bool): allowHostPorts determines if the policy allows host ports in the
              containers.

            allow_privilege_escalation (Any): allowPrivilegeEscalation determines if a pod can request to allow
              privilege escalation. If unspecified, defaults to true.

            allow_privileged_container (bool): allowPrivilegedContainer determines if a container can request to be
              run as privileged.

            allowed_capabilities (Any): allowedCapabilities is a list of capabilities that can be requested to
              add to the container. Capabilities in this field maybe added at
              the pod author's discretion. You must not list a capability in
              both AllowedCapabilities and RequiredDropCapabilities. To allow
              all capabilities you may use '*'.

            allowed_flex_volumes (Any): allowedFlexVolumes is a whitelist of allowed Flexvolumes.  Empty or
              nil indicates that all Flexvolumes may be used.  This parameter is
              effective only when the usage of the Flexvolumes is allowed in the
              "Volumes" field.

            allowed_unsafe_sysctls (Any): allowedUnsafeSysctls is a list of explicitly allowed unsafe sysctls,
              defaults to none. Each entry is either a plain sysctl name or ends
              in "*" in which case it is considered as a prefix of allowed
              sysctls. Single * means all unsafe sysctls are allowed. Kubelet
              has to whitelist all allowed unsafe sysctls explicitly to avoid
              rejection.  Examples: e.g. "foo/*" allows "foo/bar", "foo/baz",
              etc. e.g. "foo.*" allows "foo.bar", "foo.baz", etc.

            default_add_capabilities (Any): defaultAddCapabilities is the default set of capabilities that will be
              added to the container unless the pod spec specifically drops the
              capability.  You may not list a capabiility in both
              DefaultAddCapabilities and RequiredDropCapabilities.

            default_allow_privilege_escalation (Any): defaultAllowPrivilegeEscalation controls the default setting for
              whether a process can gain more privileges than its parent
              process.

            forbidden_sysctls (Any): forbiddenSysctls is a list of explicitly forbidden sysctls, defaults
              to none. Each entry is either a plain sysctl name or ends in "*"
              in which case it is considered as a prefix of forbidden sysctls.
              Single * means all sysctls are forbidden.  Examples: e.g. "foo/*"
              forbids "foo/bar", "foo/baz", etc. e.g. "foo.*" forbids "foo.bar",
              "foo.baz", etc.

            fs_group (Any): fsGroup is the strategy that will dictate what fs group is used by the
              SecurityContext.

            groups (Any): The groups that have permission to use this security context
              constraints

            priority (Any): priority influences the sort order of SCCs when evaluating which SCCs
              to try first for a given pod request based on access in the Users
              and Groups fields.  The higher the int, the higher priority. An
              unset value is considered a 0 priority. If scores for multiple
              SCCs are equal they will be sorted from most restrictive to least
              restrictive. If both priorities and restrictions are equal the
              SCCs will be sorted by name.

            read_only_root_filesystem (bool): readOnlyRootFilesystem when set to true will force containers to run
              with a read only root file system.  If the container specifically
              requests to run with a non-read only root file system the SCC
              should deny the pod. If set to false the container may run with a
              read only root file system if it wishes but it will not be forced
              to.

            required_drop_capabilities (Any): requiredDropCapabilities are the capabilities that will be dropped
              from the container.  These are required to be dropped and cannot
              be added.

            run_as_user (Any): runAsUser is the strategy that will dictate what RunAsUser is used in
              the SecurityContext.

            se_linux_context (Any): seLinuxContext is the strategy that will dictate what labels will be
              set in the SecurityContext.

            seccomp_profiles (Any): seccompProfiles lists the allowed profiles that may be set for the pod
              or container's seccomp annotations.  An unset (nil) or empty value
              means that no profiles may be specifid by the pod or container.
              The wildcard '*' may be used to allow all profiles.  When used to
              generate a value for a pod the first non-wildcard profile will be
              used as the default.

            supplemental_groups (Any): supplementalGroups is the strategy that will dictate what supplemental
              groups are used by the SecurityContext.

            users (Any): The users who have permissions to use this security context
              constraints

            volumes (Any): volumes is a white list of allowed volume plugins.  FSType corresponds
              directly with the field names of a VolumeSource (azureFile,
              configMap, emptyDir).  To allow all volumes you may use "*". To
              allow no volumes, set to ["none"].

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

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.allow_host_dir_volume_plugin is None:
                raise MissingRequiredArgumentError(argument="self.allow_host_dir_volume_plugin")

            if self.allow_host_ipc is None:
                raise MissingRequiredArgumentError(argument="self.allow_host_ipc")

            if self.allow_host_network is None:
                raise MissingRequiredArgumentError(argument="self.allow_host_network")

            if self.allow_host_pid is None:
                raise MissingRequiredArgumentError(argument="self.allow_host_pid")

            if self.allow_host_ports is None:
                raise MissingRequiredArgumentError(argument="self.allow_host_ports")

            if self.allow_privileged_container is None:
                raise MissingRequiredArgumentError(argument="self.allow_privileged_container")

            if self.read_only_root_filesystem is None:
                raise MissingRequiredArgumentError(argument="self.read_only_root_filesystem")

            self.res["allowHostDirVolumePlugin"] = self.allow_host_dir_volume_plugin
            self.res["allowHostIPC"] = self.allow_host_ipc
            self.res["allowHostNetwork"] = self.allow_host_network
            self.res["allowHostPID"] = self.allow_host_pid
            self.res["allowHostPorts"] = self.allow_host_ports
            self.res["allowPrivilegedContainer"] = self.allow_privileged_container
            self.res["readOnlyRootFilesystem"] = self.read_only_root_filesystem

            if self.allow_privilege_escalation is not None:
                self.res["allowPrivilegeEscalation"] = self.allow_privilege_escalation

            if self.allowed_capabilities is not None:
                self.res["allowedCapabilities"] = self.allowed_capabilities

            if self.allowed_flex_volumes is not None:
                self.res["allowedFlexVolumes"] = self.allowed_flex_volumes

            if self.allowed_unsafe_sysctls is not None:
                self.res["allowedUnsafeSysctls"] = self.allowed_unsafe_sysctls

            if self.default_add_capabilities is not None:
                self.res["defaultAddCapabilities"] = self.default_add_capabilities

            if self.default_allow_privilege_escalation is not None:
                self.res["defaultAllowPrivilegeEscalation"] = self.default_allow_privilege_escalation

            if self.forbidden_sysctls is not None:
                self.res["forbiddenSysctls"] = self.forbidden_sysctls

            if self.fs_group is not None:
                self.res["fsGroup"] = self.fs_group

            if self.groups is not None:
                self.res["groups"] = self.groups

            if self.priority is not None:
                self.res["priority"] = self.priority

            if self.required_drop_capabilities is not None:
                self.res["requiredDropCapabilities"] = self.required_drop_capabilities

            if self.run_as_user is not None:
                self.res["runAsUser"] = self.run_as_user

            if self.se_linux_context is not None:
                self.res["seLinuxContext"] = self.se_linux_context

            if self.seccomp_profiles is not None:
                self.res["seccompProfiles"] = self.seccomp_profiles

            if self.supplemental_groups is not None:
                self.res["supplementalGroups"] = self.supplemental_groups

            if self.users is not None:
                self.res["users"] = self.users

            if self.volumes is not None:
                self.res["volumes"] = self.volumes

    # End of generated code
