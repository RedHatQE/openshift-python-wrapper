# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md


from typing import Any

from ocp_resources.exceptions import MissingRequiredArgumentError
from ocp_resources.resource import NamespacedResource


class Deployment(NamespacedResource):
    """
    Deployment enables declarative updates for Pods and ReplicaSets.
    """

    api_group: str = NamespacedResource.ApiGroup.APPS

    def __init__(
        self,
        min_ready_seconds: int | None = None,
        paused: bool | None = None,
        progress_deadline_seconds: int | None = None,
        replicas: int | None = None,
        revision_history_limit: int | None = None,
        selector: dict[str, Any] | None = None,
        strategy: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            min_ready_seconds (int): Minimum number of seconds for which a newly created pod should be
              ready without any of its container crashing, for it to be
              considered available. Defaults to 0 (pod will be considered
              available as soon as it is ready).

            paused (bool): Indicates that the deployment is paused.

            progress_deadline_seconds (int): The maximum time in seconds for a deployment to make progress before
              it is considered to be failed. The deployment controller will
              continue to process failed deployments and a condition with a
              ProgressDeadlineExceeded reason will be surfaced in the deployment
              status. Note that progress will not be estimated during the time a
              deployment is paused. Defaults to 600s.

            replicas (int): Number of desired pods. This is a pointer to distinguish between
              explicit zero and not specified. Defaults to 1.

            revision_history_limit (int): The number of old ReplicaSets to retain to allow rollback. This is a
              pointer to distinguish between explicit zero and not specified.
              Defaults to 10.

            selector (dict[str, Any]): matchExpressions key operator values matchLabels.

            strategy (dict[str, Any]): rollingUpdate maxSurge maxUnavailable type enum: Recreate,
              RollingUpdate.

            template (dict[str, Any]): metadata annotations creationTimestamp deletionGracePeriodSeconds
              deletionTimestamp finalizers generateName generation labels
              managedFields apiVersion fieldsType fieldsV1 manager operation
              subresource time name namespace ownerReferences apiVersion
              blockOwnerDeletion controller kind name uid resourceVersion
              selfLink uid spec activeDeadlineSeconds affinity nodeAffinity
              preferredDuringSchedulingIgnoredDuringExecution preference
              matchExpressions key operator enum: DoesNotExist, Exists, Gt, In,
              .... values matchFields key operator enum: DoesNotExist, Exists,
              Gt, In, .... values weight
              requiredDuringSchedulingIgnoredDuringExecution nodeSelectorTerms
              matchExpressions key operator enum: DoesNotExist, Exists, Gt, In,
              .... values matchFields key operator enum: DoesNotExist, Exists,
              Gt, In, .... values podAffinity
              preferredDuringSchedulingIgnoredDuringExecution podAffinityTerm
              labelSelector matchExpressions key operator values matchLabels
              matchLabelKeys mismatchLabelKeys namespaceSelector
              matchExpressions key operator values matchLabels namespaces
              topologyKey weight requiredDuringSchedulingIgnoredDuringExecution
              labelSelector matchExpressions key operator values matchLabels
              matchLabelKeys mismatchLabelKeys namespaceSelector
              matchExpressions key operator values matchLabels namespaces
              topologyKey podAntiAffinity
              preferredDuringSchedulingIgnoredDuringExecution podAffinityTerm
              labelSelector matchExpressions key operator values matchLabels
              matchLabelKeys mismatchLabelKeys namespaceSelector
              matchExpressions key operator values matchLabels namespaces
              topologyKey weight requiredDuringSchedulingIgnoredDuringExecution
              labelSelector matchExpressions key operator values matchLabels
              matchLabelKeys mismatchLabelKeys namespaceSelector
              matchExpressions key operator values matchLabels namespaces
              topologyKey automountServiceAccountToken containers args command
              env name value valueFrom configMapKeyRef key name fieldRef
              apiVersion fieldPath resourceFieldRef containerName divisor
              resource secretKeyRef key name envFrom configMapRef name prefix
              secretRef name image imagePullPolicy enum: Always, IfNotPresent,
              Never lifecycle postStart exec command httpGet host httpHeaders
              name value path port scheme enum: HTTP, HTTPS sleep seconds
              tcpSocket host port preStop exec command httpGet host httpHeaders
              name value path port scheme enum: HTTP, HTTPS sleep seconds
              tcpSocket host port stopSignal enum: SIGABRT, SIGALRM, SIGBUS,
              SIGCHLD, .... livenessProbe exec command failureThreshold grpc
              port service httpGet host httpHeaders name value path port scheme
              enum: HTTP, HTTPS initialDelaySeconds periodSeconds
              successThreshold tcpSocket host port terminationGracePeriodSeconds
              timeoutSeconds name ports containerPort hostIP hostPort name
              protocol enum: SCTP, TCP, UDP readinessProbe exec command
              failureThreshold grpc port service httpGet host httpHeaders name
              value path port scheme enum: HTTP, HTTPS initialDelaySeconds
              periodSeconds successThreshold tcpSocket host port
              terminationGracePeriodSeconds timeoutSeconds resizePolicy
              resourceName restartPolicy resources claims name request limits
              requests restartPolicy securityContext allowPrivilegeEscalation
              appArmorProfile localhostProfile type enum: Localhost,
              RuntimeDefault, Unconfined capabilities add drop privileged
              procMount enum: Default, Unmasked readOnlyRootFilesystem
              runAsGroup runAsNonRoot runAsUser seLinuxOptions level role type
              user seccompProfile localhostProfile type enum: Localhost,
              RuntimeDefault, Unconfined windowsOptions gmsaCredentialSpec
              gmsaCredentialSpecName hostProcess runAsUserName startupProbe exec
              command failureThreshold grpc port service httpGet host
              httpHeaders name value path port scheme enum: HTTP, HTTPS
              initialDelaySeconds periodSeconds successThreshold tcpSocket host
              port terminationGracePeriodSeconds timeoutSeconds stdin stdinOnce
              terminationMessagePath terminationMessagePolicy enum:
              FallbackToLogsOnError, File tty volumeDevices devicePath name
              volumeMounts mountPath mountPropagation enum: Bidirectional,
              HostToContainer, None name readOnly recursiveReadOnly subPath
              subPathExpr workingDir dnsConfig nameservers options name value
              searches dnsPolicy enum: ClusterFirst, ClusterFirstWithHostNet,
              Default, None enableServiceLinks ephemeralContainers args command
              env name value valueFrom configMapKeyRef key name fieldRef
              apiVersion fieldPath resourceFieldRef containerName divisor
              resource secretKeyRef key name envFrom configMapRef name prefix
              secretRef name image imagePullPolicy enum: Always, IfNotPresent,
              Never lifecycle postStart exec command httpGet host httpHeaders
              name value path port scheme enum: HTTP, HTTPS sleep seconds
              tcpSocket host port preStop exec command httpGet host httpHeaders
              name value path port scheme enum: HTTP, HTTPS sleep seconds
              tcpSocket host port stopSignal enum: SIGABRT, SIGALRM, SIGBUS,
              SIGCHLD, .... livenessProbe exec command failureThreshold grpc
              port service httpGet host httpHeaders name value path port scheme
              enum: HTTP, HTTPS initialDelaySeconds periodSeconds
              successThreshold tcpSocket host port terminationGracePeriodSeconds
              timeoutSeconds name ports containerPort hostIP hostPort name
              protocol enum: SCTP, TCP, UDP readinessProbe exec command
              failureThreshold grpc port service httpGet host httpHeaders name
              value path port scheme enum: HTTP, HTTPS initialDelaySeconds
              periodSeconds successThreshold tcpSocket host port
              terminationGracePeriodSeconds timeoutSeconds resizePolicy
              resourceName restartPolicy resources claims name request limits
              requests restartPolicy securityContext allowPrivilegeEscalation
              appArmorProfile localhostProfile type enum: Localhost,
              RuntimeDefault, Unconfined capabilities add drop privileged
              procMount enum: Default, Unmasked readOnlyRootFilesystem
              runAsGroup runAsNonRoot runAsUser seLinuxOptions level role type
              user seccompProfile localhostProfile type enum: Localhost,
              RuntimeDefault, Unconfined windowsOptions gmsaCredentialSpec
              gmsaCredentialSpecName hostProcess runAsUserName startupProbe exec
              command failureThreshold grpc port service httpGet host
              httpHeaders name value path port scheme enum: HTTP, HTTPS
              initialDelaySeconds periodSeconds successThreshold tcpSocket host
              port terminationGracePeriodSeconds timeoutSeconds stdin stdinOnce
              targetContainerName terminationMessagePath
              terminationMessagePolicy enum: FallbackToLogsOnError, File tty
              volumeDevices devicePath name volumeMounts mountPath
              mountPropagation enum: Bidirectional, HostToContainer, None name
              readOnly recursiveReadOnly subPath subPathExpr workingDir
              hostAliases hostnames ip hostIPC hostNetwork hostPID hostUsers
              hostname imagePullSecrets name initContainers args command env
              name value valueFrom configMapKeyRef key name fieldRef apiVersion
              fieldPath resourceFieldRef containerName divisor resource
              secretKeyRef key name envFrom configMapRef name prefix secretRef
              name image imagePullPolicy enum: Always, IfNotPresent, Never
              lifecycle postStart exec command httpGet host httpHeaders name
              value path port scheme enum: HTTP, HTTPS sleep seconds tcpSocket
              host port preStop exec command httpGet host httpHeaders name value
              path port scheme enum: HTTP, HTTPS sleep seconds tcpSocket host
              port stopSignal enum: SIGABRT, SIGALRM, SIGBUS, SIGCHLD, ....
              livenessProbe exec command failureThreshold grpc port service
              httpGet host httpHeaders name value path port scheme enum: HTTP,
              HTTPS initialDelaySeconds periodSeconds successThreshold tcpSocket
              host port terminationGracePeriodSeconds timeoutSeconds name ports
              containerPort hostIP hostPort name protocol enum: SCTP, TCP, UDP
              readinessProbe exec command failureThreshold grpc port service
              httpGet host httpHeaders name value path port scheme enum: HTTP,
              HTTPS initialDelaySeconds periodSeconds successThreshold tcpSocket
              host port terminationGracePeriodSeconds timeoutSeconds
              resizePolicy resourceName restartPolicy resources claims name
              request limits requests restartPolicy securityContext
              allowPrivilegeEscalation appArmorProfile localhostProfile type
              enum: Localhost, RuntimeDefault, Unconfined capabilities add drop
              privileged procMount enum: Default, Unmasked
              readOnlyRootFilesystem runAsGroup runAsNonRoot runAsUser
              seLinuxOptions level role type user seccompProfile
              localhostProfile type enum: Localhost, RuntimeDefault, Unconfined
              windowsOptions gmsaCredentialSpec gmsaCredentialSpecName
              hostProcess runAsUserName startupProbe exec command
              failureThreshold grpc port service httpGet host httpHeaders name
              value path port scheme enum: HTTP, HTTPS initialDelaySeconds
              periodSeconds successThreshold tcpSocket host port
              terminationGracePeriodSeconds timeoutSeconds stdin stdinOnce
              terminationMessagePath terminationMessagePolicy enum:
              FallbackToLogsOnError, File tty volumeDevices devicePath name
              volumeMounts mountPath mountPropagation enum: Bidirectional,
              HostToContainer, None name readOnly recursiveReadOnly subPath
              subPathExpr workingDir nodeName nodeSelector os name overhead
              preemptionPolicy enum: Never, PreemptLowerPriority priority
              priorityClassName readinessGates conditionType resourceClaims name
              resourceClaimName resourceClaimTemplateName resources claims name
              request limits requests restartPolicy enum: Always, Never,
              OnFailure runtimeClassName schedulerName schedulingGates name
              securityContext appArmorProfile localhostProfile type enum:
              Localhost, RuntimeDefault, Unconfined fsGroup fsGroupChangePolicy
              enum: Always, OnRootMismatch runAsGroup runAsNonRoot runAsUser
              seLinuxChangePolicy seLinuxOptions level role type user
              seccompProfile localhostProfile type enum: Localhost,
              RuntimeDefault, Unconfined supplementalGroups
              supplementalGroupsPolicy enum: Merge, Strict sysctls name value
              windowsOptions gmsaCredentialSpec gmsaCredentialSpecName
              hostProcess runAsUserName serviceAccount serviceAccountName
              setHostnameAsFQDN shareProcessNamespace subdomain
              terminationGracePeriodSeconds tolerations effect enum: NoExecute,
              NoSchedule, PreferNoSchedule key operator enum: Equal, Exists
              tolerationSeconds value topologySpreadConstraints labelSelector
              matchExpressions key operator values matchLabels matchLabelKeys
              maxSkew minDomains nodeAffinityPolicy enum: Honor, Ignore
              nodeTaintsPolicy enum: Honor, Ignore topologyKey whenUnsatisfiable
              enum: DoNotSchedule, ScheduleAnyway volumes awsElasticBlockStore
              fsType partition readOnly volumeID azureDisk cachingMode enum:
              None, ReadOnly, ReadWrite diskName diskURI fsType kind enum:
              Dedicated, Managed, Shared readOnly azureFile readOnly secretName
              shareName cephfs monitors path readOnly secretFile secretRef name
              user cinder fsType readOnly secretRef name volumeID configMap
              defaultMode items key mode path name csi driver fsType
              nodePublishSecretRef name readOnly volumeAttributes downwardAPI
              defaultMode items fieldRef apiVersion fieldPath mode path
              resourceFieldRef containerName divisor resource emptyDir medium
              sizeLimit ephemeral volumeClaimTemplate metadata annotations
              creationTimestamp deletionGracePeriodSeconds deletionTimestamp
              finalizers generateName generation labels managedFields apiVersion
              fieldsType fieldsV1 manager operation subresource time name
              namespace ownerReferences apiVersion blockOwnerDeletion controller
              kind name uid resourceVersion selfLink uid spec accessModes
              dataSource apiGroup kind name dataSourceRef apiGroup kind name
              namespace resources limits requests selector matchExpressions key
              operator values matchLabels storageClassName
              volumeAttributesClassName volumeMode enum: Block, Filesystem
              volumeName fc fsType lun readOnly targetWWNs wwids flexVolume
              driver fsType options readOnly secretRef name flocker datasetName
              datasetUUID gcePersistentDisk fsType partition pdName readOnly
              gitRepo directory repository revision glusterfs endpoints path
              readOnly hostPath path type enum: "", BlockDevice, CharDevice,
              Directory, .... image pullPolicy enum: Always, IfNotPresent, Never
              reference iscsi chapAuthDiscovery chapAuthSession fsType
              initiatorName iqn iscsiInterface lun portals readOnly secretRef
              name targetPortal name nfs path readOnly server
              persistentVolumeClaim claimName readOnly photonPersistentDisk
              fsType pdID portworxVolume fsType readOnly volumeID projected
              defaultMode sources clusterTrustBundle labelSelector
              matchExpressions key operator values matchLabels name path
              signerName configMap items key mode path name downwardAPI items
              fieldRef apiVersion fieldPath mode path resourceFieldRef
              containerName divisor resource secret items key mode path name
              serviceAccountToken audience expirationSeconds path quobyte group
              readOnly registry tenant user volume rbd fsType image keyring
              monitors pool readOnly secretRef name user scaleIO fsType gateway
              protectionDomain readOnly secretRef name sslEnabled storageMode
              storagePool system volumeName secret defaultMode items key mode
              path optional secretName storageos fsType readOnly secretRef name
              volumeName volumeNamespace vsphereVolume fsType storagePolicyID
              storagePolicyName volumePath.

        """
        super().__init__(**kwargs)

        self.min_ready_seconds = min_ready_seconds
        self.paused = paused
        self.progress_deadline_seconds = progress_deadline_seconds
        self.replicas = replicas
        self.revision_history_limit = revision_history_limit
        self.selector = selector
        self.strategy = strategy
        self.template = template

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            if self.selector is None:
                raise MissingRequiredArgumentError(argument="self.selector")

            if self.template is None:
                raise MissingRequiredArgumentError(argument="self.template")

            self.res["spec"] = {}
            _spec = self.res["spec"]

            _spec["selector"] = self.selector
            _spec["template"] = self.template

            if self.min_ready_seconds is not None:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.paused is not None:
                _spec["paused"] = self.paused

            if self.progress_deadline_seconds is not None:
                _spec["progressDeadlineSeconds"] = self.progress_deadline_seconds

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.revision_history_limit is not None:
                _spec["revisionHistoryLimit"] = self.revision_history_limit

            if self.strategy is not None:
                _spec["strategy"] = self.strategy

    # End of generated code
