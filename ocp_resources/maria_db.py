# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class MariaDB(NamespacedResource):
    """
    MariaDB is the Schema for the mariadbs API. It is used to define MariaDB
    clusters.

    https://github.com/mariadb-operator/mariadb-operator/blob/main/api/v1alpha1/mariadb_types.go
    """

    api_group: str = NamespacedResource.ApiGroup.K8S_MARIADB_COM

    def __init__(
        self,
        affinity: Optional[Dict[str, Any]] = None,
        args: Optional[List[str]] = None,
        bootstrap_from: Optional[Dict[str, Any]] = None,
        command: Optional[List[str]] = None,
        connection: Optional[Dict[str, Any]] = None,
        database: Optional[str] = "",
        env: Optional[List[Any]] = None,
        env_from: Optional[List[Any]] = None,
        galera: Optional[Dict[str, Any]] = None,
        image: Optional[str] = "",
        image_pull_policy: Optional[str] = "",
        image_pull_secrets: Optional[List[Any]] = None,
        inherit_metadata: Optional[Dict[str, Any]] = None,
        init_containers: Optional[List[Any]] = None,
        liveness_probe: Optional[Dict[str, Any]] = None,
        max_scale: Optional[Dict[str, Any]] = None,
        max_scale_ref: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        my_cnf: Optional[str] = "",
        my_cnf_config_map_key_ref: Optional[Dict[str, Any]] = None,
        node_selector: Optional[Dict[str, str]] = None,
        password_secret_key_ref: Optional[Dict[str, Any]] = None,
        pod_disruption_budget: Optional[Dict[str, Any]] = None,
        pod_metadata: Optional[Dict[str, Any]] = None,
        pod_security_context: Optional[Dict[str, Any]] = None,
        port: Optional[int] = None,
        primary_connection: Optional[Dict[str, Any]] = None,
        primary_service: Optional[Dict[str, Any]] = None,
        priority_class_name: Optional[str] = "",
        readiness_probe: Optional[Dict[str, Any]] = None,
        replicas: Optional[int] = None,
        replication: Optional[Dict[str, Any]] = None,
        resources: Optional[Dict[str, Any]] = None,
        root_empty_password: Optional[bool] = None,
        root_password_secret_key_ref: Optional[Dict[str, Any]] = None,
        secondary_connection: Optional[Dict[str, Any]] = None,
        secondary_service: Optional[Dict[str, Any]] = None,
        security_context: Optional[Dict[str, Any]] = None,
        service: Optional[Dict[str, Any]] = None,
        service_account_name: Optional[str] = "",
        sidecar_containers: Optional[List[Any]] = None,
        storage: Optional[Dict[str, Any]] = None,
        tolerations: Optional[List[Any]] = None,
        topology_spread_constraints: Optional[List[Any]] = None,
        update_strategy: Optional[Dict[str, Any]] = None,
        username: Optional[str] = "",
        volume_mounts: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            affinity(Dict[str, Any]): Affinity to be used in the Pod.

              FIELDS:
                antiAffinityEnabled	<boolean>
                  AntiAffinityEnabled configures PodAntiAffinity so each Pod is scheduled in a
                  different Node, enabling HA.
                  Make sure you have at least as many Nodes available as the replicas to not
                  end up with unscheduled Pods.

                nodeAffinity	<Object>
                  Describes node affinity scheduling rules for the pod.

                podAffinity	<Object>
                  Describes pod affinity scheduling rules (e.g. co-locate this pod in the same
                  node, zone, etc. as some other pod(s)).

                podAntiAffinity	<Object>
                  Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in
                  the same node, zone, etc. as some other pod(s)).

            args(List[str]): Args to be used in the Container.

            bootstrap_from(Dict[str, Any]): BootstrapFrom defines a source to bootstrap from.

              FIELDS:
                backupRef	<Object>
                  BackupRef is a reference to a Backup object. It has priority over S3 and
                  Volume.

                restoreJob	<Object>
                  RestoreJob defines additional properties for the Job used to perform the
                  Restore.

                s3	<Object>
                  S3 defines the configuration to restore backups from a S3 compatible
                  storage. It has priority over Volume.

                targetRecoveryTime	<string>
                  TargetRecoveryTime is a RFC3339 (1970-01-01T00:00:00Z) date and time that
                  defines the point in time recovery objective.
                  It is used to determine the closest restoration source in time.

                volume	<Object>
                  Volume is a Kubernetes Volume object that contains a backup.

            command(List[str]): Command to be used in the Container.

            connection(Dict[str, Any]): Connection defines templates to configure the general Connection object.

              FIELDS:
                healthCheck	<Object>
                  HealthCheck to be used in the Connection.

                params	<map[string]string>
                  Params to be used in the Connection.

                port	<integer>
                  Port to connect to. If not provided, it defaults to the MariaDB port or to
                  the first MaxScale listener.

                secretName	<string>
                  SecretName to be used in the Connection.

                secretTemplate	<Object>
                  SecretTemplate to be used in the Connection.

                serviceName	<string>
                  ServiceName to be used in the Connection.

            database(str): Database is the initial database to be created by the operator once MariaDB
              is ready.

            env(List[Any]): Env represents the environment variables to be injected in a container.
              EnvVar represents an environment variable present in a Container.

              FIELDS:
                name	<string> -required-
                  Name of the environment variable. Must be a C_IDENTIFIER.

                value	<string>
                  Variable references $(VAR_NAME) are expanded
                  using the previously defined environment variables in the container and
                  any service environment variables. If a variable cannot be resolved,
                  the reference in the input string will be unchanged. Double $$ are reduced
                  to a single $, which allows for escaping the $(VAR_NAME) syntax: i.e.
                  "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)".
                  Escaped references will never be expanded, regardless of whether the
                  variable
                  exists or not.
                  Defaults to "".

                valueFrom	<Object>
                  Source for the environment variable's value. Cannot be used if value is not
                  empty.

            env_from(List[Any]): EnvFrom represents the references (via ConfigMap and Secrets) to environment
              variables to be injected in the container.
              EnvFromSource represents the source of a set of ConfigMaps

              FIELDS:
                configMapRef	<Object>
                  The ConfigMap to select from

                prefix	<string>
                  An optional identifier to prepend to each key in the ConfigMap. Must be a
                  C_IDENTIFIER.

                secretRef	<Object>
                  The Secret to select from

            galera(Dict[str, Any]): Replication configures high availability via Galera.

              FIELDS:
                agent	<Object>
                  GaleraAgent is a sidecar agent that co-operates with mariadb-operator.

                availableWhenDonor	<boolean>
                  AvailableWhenDonor indicates whether a donor node should be responding to
                  queries. It defaults to false.

                config	<Object>
                  GaleraConfig defines storage options for the Galera configuration files.

                enabled	<boolean>
                  Enabled is a flag to enable Galera.

                galeraLibPath	<string>
                  GaleraLibPath is a path inside the MariaDB image to the wsrep provider
                  plugin. It is defaulted if not provided.
                  More info:
                  https://galeracluster.com/library/documentation/mysql-wsrep-options.html#wsrep-provider.

                initContainer	<Object>
                  InitContainer is an init container that co-operates with mariadb-operator.

                initJob	<Object>
                  InitJob defines additional properties for the Job used to perform the
                  initialization.

                primary	<Object>
                  Primary is the Galera configuration for the primary node.

                providerOptions	<map[string]string>
                  ProviderOptions is map of Galera configuration parameters.
                  More info:
                  https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_provider_options.

                recovery	<Object>
                  GaleraRecovery is the recovery process performed by the operator whenever
                  the Galera cluster is not healthy.
                  More info:
                  https://galeracluster.com/library/documentation/crash-recovery.html.

                replicaThreads	<integer>
                  ReplicaThreads is the number of replica threads used to apply Galera write
                  sets in parallel.
                  More info:
                  https://mariadb.com/kb/en/galera-cluster-system-variables/#wsrep_slave_threads.

                sst	<string>
                  SST is the Snapshot State Transfer used when new Pods join the cluster.
                  More info: https://galeracluster.com/library/documentation/sst.html.

            image(str): Image name to be used by the MariaDB instances. The supported format is
              `<image>:<tag>`.
              Only MariaDB official images are supported.

            image_pull_policy(str): ImagePullPolicy is the image pull policy. One of `Always`, `Never` or
              `IfNotPresent`. If not defined, it defaults to `IfNotPresent`.

            image_pull_secrets(List[Any]): ImagePullSecrets is the list of pull Secrets to be used to pull the image.
              LocalObjectReference contains enough information to let you locate the
              referenced object inside the same namespace.

              FIELDS:
                name	<string>
                  Name of the referent.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
                  TODO: Add other useful fields. apiVersion, kind, uid?

            inherit_metadata(Dict[str, Any]): InheritMetadata defines the metadata to be inherited by children resources.

              FIELDS:
                annotations	<map[string]string>
                  Annotations to be added to children resources.

                labels	<map[string]string>
                  Labels to be added to children resources.

            init_containers(List[Any]): InitContainers to be used in the Pod.
              Container object definition.

              FIELDS:
                args	<[]string>
                  Args to be used in the Container.

                command	<[]string>
                  Command to be used in the Container.

                env	<[]Object>
                  Env represents the environment variables to be injected in a container.

                envFrom	<[]Object>
                  EnvFrom represents the references (via ConfigMap and Secrets) to environment
                  variables to be injected in the container.

                image	<string> -required-
                  Image name to be used by the MariaDB instances. The supported format is
                  `<image>:<tag>`.

                imagePullPolicy	<string>
                  ImagePullPolicy is the image pull policy. One of `Always`, `Never` or
                  `IfNotPresent`. If not defined, it defaults to `IfNotPresent`.

                livenessProbe	<Object>
                  LivenessProbe to be used in the Container.

                readinessProbe	<Object>
                  ReadinessProbe to be used in the Container.

                resources	<Object>
                  Resouces describes the compute resource requirements.

                securityContext	<Object>
                  SecurityContext holds security configuration that will be applied to a
                  container.

                volumeMounts	<[]Object>
                  VolumeMounts to be used in the Container.

            liveness_probe(Dict[str, Any]): LivenessProbe to be used in the Container.

              FIELDS:
                exec	<Object>
                  Exec specifies the action to take.

                failureThreshold	<integer>
                  Minimum consecutive failures for the probe to be considered failed after
                  having succeeded.
                  Defaults to 3. Minimum value is 1.

                grpc	<Object>
                  GRPC specifies an action involving a GRPC port.

                httpGet	<Object>
                  HTTPGet specifies the http request to perform.

                initialDelaySeconds	<integer>
                  Number of seconds after the container has started before liveness probes are
                  initiated.
                  More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                periodSeconds	<integer>
                  How often (in seconds) to perform the probe.
                  Default to 10 seconds. Minimum value is 1.

                successThreshold	<integer>
                  Minimum consecutive successes for the probe to be considered successful
                  after having failed.
                  Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1.

                tcpSocket	<Object>
                  TCPSocket specifies an action involving a TCP port.

                terminationGracePeriodSeconds	<integer>
                  Optional duration in seconds the pod needs to terminate gracefully upon
                  probe failure.
                  The grace period is the duration in seconds after the processes running in
                  the pod are sent
                  a termination signal and the time when the processes are forcibly halted
                  with a kill signal.
                  Set this value longer than the expected cleanup time for your process.
                  If this value is nil, the pod's terminationGracePeriodSeconds will be used.
                  Otherwise, this
                  value overrides the value provided by the pod spec.
                  Value must be non-negative integer. The value zero indicates stop
                  immediately via
                  the kill signal (no opportunity to shut down).
                  This is a beta field and requires enabling ProbeTerminationGracePeriod
                  feature gate.
                  Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset.

                timeoutSeconds	<integer>
                  Number of seconds after which the probe times out.
                  Defaults to 1 second. Minimum value is 1.
                  More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

            max_scale(Dict[str, Any]): MaxScale is the MaxScale specification that defines the MaxScale resource to
              be used with the current MariaDB.
              When enabling this field, MaxScaleRef is automatically set.

              FIELDS:
                admin	<Object>
                  Admin configures the admin REST API and GUI.

                auth	<Object>
                  Auth defines the credentials required for MaxScale to connect to MariaDB.

                config	<Object>
                  Config defines the MaxScale configuration.

                connection	<Object>
                  Connection provides a template to define the Connection for MaxScale.

                enabled	<boolean>
                  Enabled is a flag to enable a MaxScale instance to be used with the current
                  MariaDB.

                guiKubernetesService	<Object>
                  GuiKubernetesService define a template for a Kubernetes Service object to
                  connect to MaxScale's GUI.

                image	<string>
                  Image name to be used by the MaxScale instances. The supported format is
                  `<image>:<tag>`.
                  Only MariaDB official images are supported.

                imagePullPolicy	<string>
                  ImagePullPolicy is the image pull policy. One of `Always`, `Never` or
                  `IfNotPresent`. If not defined, it defaults to `IfNotPresent`.

                kubernetesService	<Object>
                  KubernetesService defines a template for a Kubernetes Service object to
                  connect to MaxScale.

                metrics	<Object>
                  Metrics configures metrics and how to scrape them.

                monitor	<Object>
                  Monitor monitors MariaDB server instances.

                podDisruptionBudget	<Object>
                  PodDisruptionBudget defines the budget for replica availability.

                replicas	<integer>
                  Replicas indicates the number of desired instances.

                requeueInterval	<string>
                  RequeueInterval is used to perform requeue reconciliations.

                services	<[]Object>
                  Services define how the traffic is forwarded to the MariaDB servers.

                updateStrategy	<Object>
                  UpdateStrategy defines the update strategy for the StatefulSet object.

            max_scale_ref(Dict[str, Any]): MaxScaleRef is a reference to a MaxScale resource to be used with the
              current MariaDB.
              Providing this field implies delegating high availability tasks such as
              primary failover to MaxScale.

              FIELDS:
                apiVersion	<string>
                  API version of the referent.

                fieldPath	<string>
                  If referring to a piece of an object instead of an entire object, this
                  string
                  should contain a valid JSON/Go field access statement, such as
                  desiredState.manifest.containers[2].
                  For example, if the object reference is to a container within a pod, this
                  would take on a value like:
                  "spec.containers{name}" (where "name" refers to the name of the container
                  that triggered
                  the event) or if no container name is specified "spec.containers[2]"
                  (container with
                  index 2 in this pod). This syntax is chosen only to have some well-defined
                  way of
                  referencing a part of an object.

                kind	<string>
                  Kind of the referent.
                  More info:
                  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

                name	<string>
                  Name of the referent.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

                namespace	<string>
                  Namespace of the referent.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/

                resourceVersion	<string>
                  Specific resourceVersion to which this reference is made, if any.
                  More info:
                  https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency

                uid	<string>
                  UID of the referent.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids

            metrics(Dict[str, Any]): Metrics configures metrics and how to scrape them.

              FIELDS:
                enabled	<boolean>
                  Enabled is a flag to enable Metrics

                exporter	<Object>
                  Exporter defines the metrics exporter container.

                passwordSecretKeyRef	<Object>
                  PasswordSecretKeyRef is a reference to the password of the monitoring user
                  used by the exporter.
                  If the referred Secret is labeled with "k8s.mariadb.com/watch", updates may
                  be performed to the Secret in order to update the password.

                serviceMonitor	<Object>
                  ServiceMonitor defines the ServiceMonior object.

                username	<string>
                  Username is the username of the monitoring user used by the exporter.

            my_cnf(str): MyCnf allows to specify the my.cnf file mounted by Mariadb.
              Updating this field will trigger an update to the Mariadb resource.

            my_cnf_config_map_key_ref(Dict[str, Any]): MyCnfConfigMapKeyRef is a reference to the my.cnf config file provided via a
              ConfigMap.
              If not provided, it will be defaulted with a reference to a ConfigMap
              containing the MyCnf field.
              If the referred ConfigMap is labeled with "k8s.mariadb.com/watch", an update
              to the Mariadb resource will be triggered when the ConfigMap is updated.

              FIELDS:
                key	<string> -required-
                  The key to select.

                name	<string>
                  Name of the referent.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

                optional	<boolean>
                  Specify whether the ConfigMap or its key must be defined

            node_selector(Dict[str, str]): NodeSelector to be used in the Pod.

            password_secret_key_ref(Dict[str, Any]): PasswordSecretKeyRef is a reference to a Secret that contains the password
              for the initial user.
              If the referred Secret is labeled with "k8s.mariadb.com/watch", updates may
              be performed to the Secret in order to update the password.

              FIELDS:
                generate	<boolean>
                  Generate indicates whether the Secret should be generated if the Secret
                  referenced is not present.

                key	<string> -required-
                  The key of the secret to select from.  Must be a valid secret key.

                name	<string>
                  Name of the referent.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

                optional	<boolean>
                  Specify whether the Secret or its key must be defined

            pod_disruption_budget(Dict[str, Any]): PodDisruptionBudget defines the budget for replica availability.

              FIELDS:
                maxUnavailable	<Object>
                  MaxUnavailable defines the number of maximum unavailable Pods.

                minAvailable	<Object>
                  MinAvailable defines the number of minimum available Pods.

            pod_metadata(Dict[str, Any]): PodMetadata defines extra metadata for the Pod.

              FIELDS:
                annotations	<map[string]string>
                  Annotations to be added to children resources.

                labels	<map[string]string>
                  Labels to be added to children resources.

            pod_security_context(Dict[str, Any]): SecurityContext holds pod-level security attributes and common container
              settings.

              FIELDS:
                fsGroup	<integer>
                  A special supplemental group that applies to all containers in a pod.
                  Some volume types allow the Kubelet to change the ownership of that volume
                  to be owned by the pod:


                  1. The owning GID will be the FSGroup
                  2. The setgid bit is set (new files created in the volume will be owned by
                  FSGroup)
                  3. The permission bits are OR'd with rw-rw----


                  If unset, the Kubelet will not modify the ownership and permissions of any
                  volume.
                  Note that this field cannot be set when spec.os.name is windows.

                fsGroupChangePolicy	<string>
                  fsGroupChangePolicy defines behavior of changing ownership and permission of
                  the volume
                  before being exposed inside Pod. This field will only apply to
                  volume types which support fsGroup based ownership(and permissions).
                  It will have no effect on ephemeral volume types such as: secret, configmaps
                  and emptydir.
                  Valid values are "OnRootMismatch" and "Always". If not specified, "Always"
                  is used.
                  Note that this field cannot be set when spec.os.name is windows.

                runAsGroup	<integer>
                  The GID to run the entrypoint of the container process.
                  Uses runtime default if unset.
                  May also be set in SecurityContext.  If set in both SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence
                  for that container.
                  Note that this field cannot be set when spec.os.name is windows.

                runAsNonRoot	<boolean>
                  Indicates that the container must run as a non-root user.
                  If true, the Kubelet will validate the image at runtime to ensure that it
                  does not run as UID 0 (root) and fail to start the container if it does.
                  If unset or false, no such validation will be performed.
                  May also be set in SecurityContext.  If set in both SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence.

                runAsUser	<integer>
                  The UID to run the entrypoint of the container process.
                  Defaults to user specified in image metadata if unspecified.
                  May also be set in SecurityContext.  If set in both SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence
                  for that container.
                  Note that this field cannot be set when spec.os.name is windows.

                seLinuxOptions	<Object>
                  The SELinux context to be applied to all containers.
                  If unspecified, the container runtime will allocate a random SELinux context
                  for each
                  container.  May also be set in SecurityContext.  If set in
                  both SecurityContext and PodSecurityContext, the value specified in
                  SecurityContext
                  takes precedence for that container.
                  Note that this field cannot be set when spec.os.name is windows.

                seccompProfile	<Object>
                  The seccomp options to use by the containers in this pod.
                  Note that this field cannot be set when spec.os.name is windows.

                supplementalGroups	<[]integer>
                  A list of groups applied to the first process run in each container, in
                  addition
                  to the container's primary GID, the fsGroup (if specified), and group
                  memberships
                  defined in the container image for the uid of the container process. If
                  unspecified,
                  no additional groups are added to any container. Note that group memberships
                  defined in the container image for the uid of the container process are
                  still effective,
                  even if they are not included in this list.
                  Note that this field cannot be set when spec.os.name is windows.

                sysctls	<[]Object>
                  Sysctls hold a list of namespaced sysctls used for the pod. Pods with
                  unsupported
                  sysctls (by the container runtime) might fail to launch.
                  Note that this field cannot be set when spec.os.name is windows.

                windowsOptions	<Object>
                  The Windows specific settings applied to all containers.
                  If unspecified, the options within a container's SecurityContext will be
                  used.
                  If set in both SecurityContext and PodSecurityContext, the value specified
                  in SecurityContext takes precedence.
                  Note that this field cannot be set when spec.os.name is linux.

            port(int): Port where the instances will be listening for connections.

            primary_connection(Dict[str, Any]): PrimaryConnection defines templates to configure the primary Connection
              object.

              FIELDS:
                healthCheck	<Object>
                  HealthCheck to be used in the Connection.

                params	<map[string]string>
                  Params to be used in the Connection.

                port	<integer>
                  Port to connect to. If not provided, it defaults to the MariaDB port or to
                  the first MaxScale listener.

                secretName	<string>
                  SecretName to be used in the Connection.

                secretTemplate	<Object>
                  SecretTemplate to be used in the Connection.

                serviceName	<string>
                  ServiceName to be used in the Connection.

            primary_service(Dict[str, Any]): PrimaryService defines templates to configure the primary Service object.

              FIELDS:
                allocateLoadBalancerNodePorts	<boolean>
                  AllocateLoadBalancerNodePorts Service field.

                externalTrafficPolicy	<string>
                  ExternalTrafficPolicy Service field.

                loadBalancerIP	<string>
                  LoadBalancerIP Service field.

                loadBalancerSourceRanges	<[]string>
                  LoadBalancerSourceRanges Service field.

                metadata	<Object>
                  Metadata to be added to the Service metadata.

                sessionAffinity	<string>
                  SessionAffinity Service field.

                type	<string>
                  Type is the Service type. One of `ClusterIP`, `NodePort` or `LoadBalancer`.
                  If not defined, it defaults to `ClusterIP`.

            priority_class_name(str): PriorityClassName to be used in the Pod.

            readiness_probe(Dict[str, Any]): ReadinessProbe to be used in the Container.

              FIELDS:
                exec	<Object>
                  Exec specifies the action to take.

                failureThreshold	<integer>
                  Minimum consecutive failures for the probe to be considered failed after
                  having succeeded.
                  Defaults to 3. Minimum value is 1.

                grpc	<Object>
                  GRPC specifies an action involving a GRPC port.

                httpGet	<Object>
                  HTTPGet specifies the http request to perform.

                initialDelaySeconds	<integer>
                  Number of seconds after the container has started before liveness probes are
                  initiated.
                  More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                periodSeconds	<integer>
                  How often (in seconds) to perform the probe.
                  Default to 10 seconds. Minimum value is 1.

                successThreshold	<integer>
                  Minimum consecutive successes for the probe to be considered successful
                  after having failed.
                  Defaults to 1. Must be 1 for liveness and startup. Minimum value is 1.

                tcpSocket	<Object>
                  TCPSocket specifies an action involving a TCP port.

                terminationGracePeriodSeconds	<integer>
                  Optional duration in seconds the pod needs to terminate gracefully upon
                  probe failure.
                  The grace period is the duration in seconds after the processes running in
                  the pod are sent
                  a termination signal and the time when the processes are forcibly halted
                  with a kill signal.
                  Set this value longer than the expected cleanup time for your process.
                  If this value is nil, the pod's terminationGracePeriodSeconds will be used.
                  Otherwise, this
                  value overrides the value provided by the pod spec.
                  Value must be non-negative integer. The value zero indicates stop
                  immediately via
                  the kill signal (no opportunity to shut down).
                  This is a beta field and requires enabling ProbeTerminationGracePeriod
                  feature gate.
                  Minimum value is 1. spec.terminationGracePeriodSeconds is used if unset.

                timeoutSeconds	<integer>
                  Number of seconds after which the probe times out.
                  Defaults to 1 second. Minimum value is 1.
                  More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

            replicas(int): Replicas indicates the number of desired instances.

            replication(Dict[str, Any]): Replication configures high availability via replication. This feature is
              still in alpha, use Galera if you are looking for a more production-ready
              HA.

              FIELDS:
                enabled	<boolean>
                  Enabled is a flag to enable Replication.

                primary	<Object>
                  Primary is the replication configuration for the primary node.

                probesEnabled	<boolean>
                  ProbesEnabled indicates to use replication specific liveness and readiness
                  probes.
                  This probes check that the primary can receive queries and that the replica
                  has the replication thread running.

                replica	<Object>
                  ReplicaReplication is the replication configuration for the replica nodes.

                syncBinlog	<boolean>
                  SyncBinlog indicates whether the binary log should be synchronized to the
                  disk after every event.
                  It trades off performance for consistency.
                  See:
                  https://mariadb.com/kb/en/replication-and-binary-log-system-variables/#sync_binlog.

            resources(Dict[str, Any]): Resouces describes the compute resource requirements.

              FIELDS:
                claims	<[]Object>
                  Claims lists the names of resources, defined in spec.resourceClaims,
                  that are used by this container.


                  This is an alpha field and requires enabling the
                  DynamicResourceAllocation feature gate.


                  This field is immutable. It can only be set for containers.

                limits	<map[string]Object>
                  Limits describes the maximum amount of compute resources allowed.
                  More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

                requests	<map[string]Object>
                  Requests describes the minimum amount of compute resources required.
                  If Requests is omitted for a container, it defaults to Limits if that is
                  explicitly specified,
                  otherwise to an implementation-defined value. Requests cannot exceed Limits.
                  More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

            root_empty_password(bool): RootEmptyPassword indicates if the root password should be empty. Don't use
              this feature in production, it is only intended for development and test
              environments.

            root_password_secret_key_ref(Dict[str, Any]): RootPasswordSecretKeyRef is a reference to a Secret key containing the root
              password.

              FIELDS:
                generate	<boolean>
                  Generate indicates whether the Secret should be generated if the Secret
                  referenced is not present.

                key	<string> -required-
                  The key of the secret to select from.  Must be a valid secret key.

                name	<string>
                  Name of the referent.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

                optional	<boolean>
                  Specify whether the Secret or its key must be defined

            secondary_connection(Dict[str, Any]): SecondaryConnection defines templates to configure the secondary Connection
              object.

              FIELDS:
                healthCheck	<Object>
                  HealthCheck to be used in the Connection.

                params	<map[string]string>
                  Params to be used in the Connection.

                port	<integer>
                  Port to connect to. If not provided, it defaults to the MariaDB port or to
                  the first MaxScale listener.

                secretName	<string>
                  SecretName to be used in the Connection.

                secretTemplate	<Object>
                  SecretTemplate to be used in the Connection.

                serviceName	<string>
                  ServiceName to be used in the Connection.

            secondary_service(Dict[str, Any]): SecondaryService defines templates to configure the secondary Service
              object.

              FIELDS:
                allocateLoadBalancerNodePorts	<boolean>
                  AllocateLoadBalancerNodePorts Service field.

                externalTrafficPolicy	<string>
                  ExternalTrafficPolicy Service field.

                loadBalancerIP	<string>
                  LoadBalancerIP Service field.

                loadBalancerSourceRanges	<[]string>
                  LoadBalancerSourceRanges Service field.

                metadata	<Object>
                  Metadata to be added to the Service metadata.

                sessionAffinity	<string>
                  SessionAffinity Service field.

                type	<string>
                  Type is the Service type. One of `ClusterIP`, `NodePort` or `LoadBalancer`.
                  If not defined, it defaults to `ClusterIP`.

            security_context(Dict[str, Any]): SecurityContext holds security configuration that will be applied to a
              container.

              FIELDS:
                allowPrivilegeEscalation	<boolean>
                  AllowPrivilegeEscalation controls whether a process can gain more
                  privileges than its parent process. This bool directly controls if
                  the no_new_privs flag will be set on the container process.
                  AllowPrivilegeEscalation is true always when the container is:
                  1) run as Privileged
                  2) has CAP_SYS_ADMIN
                  Note that this field cannot be set when spec.os.name is windows.

                capabilities	<Object>
                  The capabilities to add/drop when running containers.
                  Defaults to the default set of capabilities granted by the container
                  runtime.
                  Note that this field cannot be set when spec.os.name is windows.

                privileged	<boolean>
                  Run container in privileged mode.
                  Processes in privileged containers are essentially equivalent to root on the
                  host.
                  Defaults to false.
                  Note that this field cannot be set when spec.os.name is windows.

                procMount	<string>
                  procMount denotes the type of proc mount to use for the containers.
                  The default is DefaultProcMount which uses the container runtime defaults
                  for
                  readonly paths and masked paths.
                  This requires the ProcMountType feature flag to be enabled.
                  Note that this field cannot be set when spec.os.name is windows.

                readOnlyRootFilesystem	<boolean>
                  Whether this container has a read-only root filesystem.
                  Default is false.
                  Note that this field cannot be set when spec.os.name is windows.

                runAsGroup	<integer>
                  The GID to run the entrypoint of the container process.
                  Uses runtime default if unset.
                  May also be set in PodSecurityContext.  If set in both SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence.
                  Note that this field cannot be set when spec.os.name is windows.

                runAsNonRoot	<boolean>
                  Indicates that the container must run as a non-root user.
                  If true, the Kubelet will validate the image at runtime to ensure that it
                  does not run as UID 0 (root) and fail to start the container if it does.
                  If unset or false, no such validation will be performed.
                  May also be set in PodSecurityContext.  If set in both SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence.

                runAsUser	<integer>
                  The UID to run the entrypoint of the container process.
                  Defaults to user specified in image metadata if unspecified.
                  May also be set in PodSecurityContext.  If set in both SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence.
                  Note that this field cannot be set when spec.os.name is windows.

                seLinuxOptions	<Object>
                  The SELinux context to be applied to the container.
                  If unspecified, the container runtime will allocate a random SELinux context
                  for each
                  container.  May also be set in PodSecurityContext.  If set in both
                  SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence.
                  Note that this field cannot be set when spec.os.name is windows.

                seccompProfile	<Object>
                  The seccomp options to use by this container. If seccomp options are
                  provided at both the pod & container level, the container options
                  override the pod options.
                  Note that this field cannot be set when spec.os.name is windows.

                windowsOptions	<Object>
                  The Windows specific settings applied to all containers.
                  If unspecified, the options from the PodSecurityContext will be used.
                  If set in both SecurityContext and PodSecurityContext, the value specified
                  in SecurityContext takes precedence.
                  Note that this field cannot be set when spec.os.name is linux.

            service(Dict[str, Any]): Service defines templates to configure the general Service object.

              FIELDS:
                allocateLoadBalancerNodePorts	<boolean>
                  AllocateLoadBalancerNodePorts Service field.

                externalTrafficPolicy	<string>
                  ExternalTrafficPolicy Service field.

                loadBalancerIP	<string>
                  LoadBalancerIP Service field.

                loadBalancerSourceRanges	<[]string>
                  LoadBalancerSourceRanges Service field.

                metadata	<Object>
                  Metadata to be added to the Service metadata.

                sessionAffinity	<string>
                  SessionAffinity Service field.

                type	<string>
                  Type is the Service type. One of `ClusterIP`, `NodePort` or `LoadBalancer`.
                  If not defined, it defaults to `ClusterIP`.

            service_account_name(str): ServiceAccountName is the name of the ServiceAccount to be used by the Pods.

            sidecar_containers(List[Any]): SidecarContainers to be used in the Pod.
              Container object definition.

              FIELDS:
                args	<[]string>
                  Args to be used in the Container.

                command	<[]string>
                  Command to be used in the Container.

                env	<[]Object>
                  Env represents the environment variables to be injected in a container.

                envFrom	<[]Object>
                  EnvFrom represents the references (via ConfigMap and Secrets) to environment
                  variables to be injected in the container.

                image	<string> -required-
                  Image name to be used by the MariaDB instances. The supported format is
                  `<image>:<tag>`.

                imagePullPolicy	<string>
                  ImagePullPolicy is the image pull policy. One of `Always`, `Never` or
                  `IfNotPresent`. If not defined, it defaults to `IfNotPresent`.

                livenessProbe	<Object>
                  LivenessProbe to be used in the Container.

                readinessProbe	<Object>
                  ReadinessProbe to be used in the Container.

                resources	<Object>
                  Resouces describes the compute resource requirements.

                securityContext	<Object>
                  SecurityContext holds security configuration that will be applied to a
                  container.

                volumeMounts	<[]Object>
                  VolumeMounts to be used in the Container.

            storage(Dict[str, Any]): Storage defines the storage options to be used for provisioning the PVCs
              mounted by MariaDB.

              FIELDS:
                ephemeral	<boolean>
                  Ephemeral indicates whether to use ephemeral storage in the PVCs. It is only
                  compatible with non HA MariaDBs.

                resizeInUseVolumes	<boolean>
                  ResizeInUseVolumes indicates whether the PVCs can be resized. The
                  'StorageClassName' used should have 'allowVolumeExpansion' set to 'true' to
                  allow resizing.
                  It defaults to true.

                size	<Object>
                  Size of the PVCs to be mounted by MariaDB. Required if not provided in
                  'VolumeClaimTemplate'. It superseeds the storage size specified in
                  'VolumeClaimTemplate'.

                storageClassName	<string>
                  StorageClassName to be used to provision the PVCS. It superseeds the
                  'StorageClassName' specified in 'VolumeClaimTemplate'.
                  If not provided, the default 'StorageClass' configured in the cluster is
                  used.

                volumeClaimTemplate	<Object>
                  VolumeClaimTemplate provides a template to define the PVCs.

                waitForVolumeResize	<boolean>
                  WaitForVolumeResize indicates whether to wait for the PVCs to be resized
                  before marking the MariaDB object as ready. This will block other operations
                  such as cluster recovery while the resize is in progress.
                  It defaults to true.

            tolerations(List[Any]): Tolerations to be used in the Pod.
              The pod this Toleration is attached to tolerates any taint that matches
              the triple <key,value,effect> using the matching operator <operator>.

              FIELDS:
                effect	<string>
                  Effect indicates the taint effect to match. Empty means match all taint
                  effects.
                  When specified, allowed values are NoSchedule, PreferNoSchedule and
                  NoExecute.

                key	<string>
                  Key is the taint key that the toleration applies to. Empty means match all
                  taint keys.
                  If the key is empty, operator must be Exists; this combination means to
                  match all values and all keys.

                operator	<string>
                  Operator represents a key's relationship to the value.
                  Valid operators are Exists and Equal. Defaults to Equal.
                  Exists is equivalent to wildcard for value, so that a pod can
                  tolerate all taints of a particular category.

                tolerationSeconds	<integer>
                  TolerationSeconds represents the period of time the toleration (which must
                  be
                  of effect NoExecute, otherwise this field is ignored) tolerates the taint.
                  By default,
                  it is not set, which means tolerate the taint forever (do not evict). Zero
                  and
                  negative values will be treated as 0 (evict immediately) by the system.

                value	<string>
                  Value is the taint value the toleration matches to.
                  If the operator is Exists, the value should be empty, otherwise just a
                  regular string.

            topology_spread_constraints(List[Any]): TopologySpreadConstraints to be used in the Pod.
              TopologySpreadConstraint specifies how to spread matching pods among the
              given topology.

              FIELDS:
                labelSelector	<Object>
                  LabelSelector is used to find matching pods.
                  Pods that match this label selector are counted to determine the number of
                  pods
                  in their corresponding topology domain.

                matchLabelKeys	<[]string>
                  MatchLabelKeys is a set of pod label keys to select the pods over which
                  spreading will be calculated. The keys are used to lookup values from the
                  incoming pod labels, those key-value labels are ANDed with labelSelector
                  to select the group of existing pods over which spreading will be calculated
                  for the incoming pod. The same key is forbidden to exist in both
                  MatchLabelKeys and LabelSelector.
                  MatchLabelKeys cannot be set when LabelSelector isn't set.
                  Keys that don't exist in the incoming pod labels will
                  be ignored. A null or empty list means only match against labelSelector.


                  This is a beta field and requires the MatchLabelKeysInPodTopologySpread
                  feature gate to be enabled (enabled by default).

                maxSkew	<integer> -required-
                  MaxSkew describes the degree to which pods may be unevenly distributed.
                  When `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted
                  difference
                  between the number of matching pods in the target topology and the global
                  minimum.
                  The global minimum is the minimum number of matching pods in an eligible
                  domain
                  or zero if the number of eligible domains is less than MinDomains.
                  For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the
                  same
                  labelSelector spread as 2/2/1:
                  In this case, the global minimum is 1.
                  | zone1 | zone2 | zone3 |
                  |  P P  |  P P  |   P   |
                  - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to become
                  2/2/2;
                  scheduling it onto zone1(zone2) would make the ActualSkew(3-1) on
                  zone1(zone2)
                  violate MaxSkew(1).
                  - if MaxSkew is 2, incoming pod can be scheduled onto any zone.
                  When `whenUnsatisfiable=ScheduleAnyway`, it is used to give higher
                  precedence
                  to topologies that satisfy it.
                  It's a required field. Default value is 1 and 0 is not allowed.

                minDomains	<integer>
                  MinDomains indicates a minimum number of eligible domains.
                  When the number of eligible domains with matching topology keys is less than
                  minDomains,
                  Pod Topology Spread treats "global minimum" as 0, and then the calculation
                  of Skew is performed.
                  And when the number of eligible domains with matching topology keys equals
                  or greater than minDomains,
                  this value has no effect on scheduling.
                  As a result, when the number of eligible domains is less than minDomains,
                  scheduler won't schedule more than maxSkew Pods to those domains.
                  If value is nil, the constraint behaves as if MinDomains is equal to 1.
                  Valid values are integers greater than 0.
                  When value is not nil, WhenUnsatisfiable must be DoNotSchedule.


                  For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to
                  5 and pods with the same
                  labelSelector spread as 2/2/2:
                  | zone1 | zone2 | zone3 |
                  |  P P  |  P P  |  P P  |
                  The number of domains is less than 5(MinDomains), so "global minimum" is
                  treated as 0.
                  In this situation, new pod with the same labelSelector cannot be scheduled,
                  because computed skew will be 3(3 - 0) if new Pod is scheduled to any of the
                  three zones,
                  it will violate MaxSkew.


                  This is a beta field and requires the MinDomainsInPodTopologySpread feature
                  gate to be enabled (enabled by default).

                nodeAffinityPolicy	<string>
                  NodeAffinityPolicy indicates how we will treat Pod's
                  nodeAffinity/nodeSelector
                  when calculating pod topology spread skew. Options are:
                  - Honor: only nodes matching nodeAffinity/nodeSelector are included in the
                  calculations.
                  - Ignore: nodeAffinity/nodeSelector are ignored. All nodes are included in
                  the calculations.


                  If this value is nil, the behavior is equivalent to the Honor policy.
                  This is a beta-level feature default enabled by the
                  NodeInclusionPolicyInPodTopologySpread feature flag.

                nodeTaintsPolicy	<string>
                  NodeTaintsPolicy indicates how we will treat node taints when calculating
                  pod topology spread skew. Options are:
                  - Honor: nodes without taints, along with tainted nodes for which the
                  incoming pod
                  has a toleration, are included.
                  - Ignore: node taints are ignored. All nodes are included.


                  If this value is nil, the behavior is equivalent to the Ignore policy.
                  This is a beta-level feature default enabled by the
                  NodeInclusionPolicyInPodTopologySpread feature flag.

                topologyKey	<string> -required-
                  TopologyKey is the key of node labels. Nodes that have a label with this key
                  and identical values are considered to be in the same topology.
                  We consider each <key, value> as a "bucket", and try to put balanced number
                  of pods into each bucket.
                  We define a domain as a particular instance of a topology.
                  Also, we define an eligible domain as a domain whose nodes meet the
                  requirements of
                  nodeAffinityPolicy and nodeTaintsPolicy.
                  e.g. If TopologyKey is "kubernetes.io/hostname", each Node is a domain of
                  that topology.
                  And, if TopologyKey is "topology.kubernetes.io/zone", each zone is a domain
                  of that topology.
                  It's a required field.

                whenUnsatisfiable	<string> -required-
                  WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy
                  the spread constraint.
                  - DoNotSchedule (default) tells the scheduler not to schedule it.
                  - ScheduleAnyway tells the scheduler to schedule the pod in any location,
                    but giving higher precedence to topologies that would help reduce the
                    skew.
                  A constraint is considered "Unsatisfiable" for an incoming pod
                  if and only if every possible node assignment for that pod would violate
                  "MaxSkew" on some topology.
                  For example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the
                  same
                  labelSelector spread as 3/1/1:
                  | zone1 | zone2 | zone3 |
                  | P P P |   P   |   P   |
                  If WhenUnsatisfiable is set to DoNotSchedule, incoming pod can only be
                  scheduled
                  to zone2(zone3) to become 3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3)
                  satisfies
                  MaxSkew(1). In other words, the cluster can still be imbalanced, but
                  scheduler
                  won't make it *more* imbalanced.
                  It's a required field.

            update_strategy(Dict[str, Any]): UpdateStrategy defines how a MariaDB resource is updated.

              FIELDS:
                rollingUpdate	<Object>
                  RollingUpdate defines parameters for the RollingUpdate type.

                type	<string>
                  Type defines the type of updates. One of `ReplicasFirstPrimaryLast`,
                  `RollingUpdate` or `OnDelete`. If not defined, it defaults to
                  `ReplicasFirstPrimaryLast`.

            username(str): Username is the initial username to be created by the operator once MariaDB
              is ready. It has all privileges on the initial database.

            volume_mounts(List[Any]): VolumeMounts to be used in the Container.
              VolumeMount describes a mounting of a Volume within a container.

              FIELDS:
                mountPath	<string> -required-
                  Path within the container at which the volume should be mounted.  Must
                  not contain ':'.

                mountPropagation	<string>
                  mountPropagation determines how mounts are propagated from the host
                  to container and the other way around.
                  When not set, MountPropagationNone is used.
                  This field is beta in 1.10.

                name	<string> -required-
                  This must match the Name of a Volume.

                readOnly	<boolean>
                  Mounted read-only if true, read-write otherwise (false or unspecified).
                  Defaults to false.

                subPath	<string>
                  Path within the volume from which the container's volume should be mounted.
                  Defaults to "" (volume's root).

                subPathExpr	<string>
                  Expanded path within the volume from which the container's volume should be
                  mounted.
                  Behaves similarly to SubPath but environment variable references $(VAR_NAME)
                  are expanded using the container's environment.
                  Defaults to "" (volume's root).
                  SubPathExpr and SubPath are mutually exclusive.

            volumes(List[Any]): Volumes to be used in the Pod.
              Volume represents a named volume in a pod that may be accessed by any
              container in the pod.

              FIELDS:
                awsElasticBlockStore	<Object>
                  awsElasticBlockStore represents an AWS Disk resource that is attached to a
                  kubelet's host machine and then exposed to the pod.
                  More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore

                azureDisk	<Object>
                  azureDisk represents an Azure Data Disk mount on the host and bind mount to
                  the pod.

                azureFile	<Object>
                  azureFile represents an Azure File Service mount on the host and bind mount
                  to the pod.

                cephfs	<Object>
                  cephFS represents a Ceph FS mount on the host that shares a pod's lifetime

                cinder	<Object>
                  cinder represents a cinder volume attached and mounted on kubelets host
                  machine.
                  More info: https://examples.k8s.io/mysql-cinder-pd/README.md

                configMap	<Object>
                  configMap represents a configMap that should populate this volume

                csi	<Object>
                  csi (Container Storage Interface) represents ephemeral storage that is
                  handled by certain external CSI drivers (Beta feature).

                downwardAPI	<Object>
                  downwardAPI represents downward API about the pod that should populate this
                  volume

                emptyDir	<Object>
                  emptyDir represents a temporary directory that shares a pod's lifetime.
                  More info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir

                ephemeral	<Object>
                  ephemeral represents a volume that is handled by a cluster storage driver.
                  The volume's lifecycle is tied to the pod that defines it - it will be
                  created before the pod starts,
                  and deleted when the pod is removed.


                  Use this if:
                  a) the volume is only needed while the pod runs,
                  b) features of normal volumes like restoring from snapshot or capacity
                     tracking are needed,
                  c) the storage driver is specified through a storage class, and
                  d) the storage driver supports dynamic volume provisioning through
                     a PersistentVolumeClaim (see EphemeralVolumeSource for more
                     information on the connection between this volume type
                     and PersistentVolumeClaim).


                  Use PersistentVolumeClaim or one of the vendor-specific
                  APIs for volumes that persist for longer than the lifecycle
                  of an individual pod.


                  Use CSI for light-weight local ephemeral volumes if the CSI driver is meant
                  to
                  be used that way - see the documentation of the driver for
                  more information.


                  A pod can use both types of ephemeral volumes and
                  persistent volumes at the same time.

                fc	<Object>
                  fc represents a Fibre Channel resource that is attached to a kubelet's host
                  machine and then exposed to the pod.

                flexVolume	<Object>
                  flexVolume represents a generic volume resource that is
                  provisioned/attached using an exec based plugin.

                flocker	<Object>
                  flocker represents a Flocker volume attached to a kubelet's host machine.
                  This depends on the Flocker control service being running

                gcePersistentDisk	<Object>
                  gcePersistentDisk represents a GCE Disk resource that is attached to a
                  kubelet's host machine and then exposed to the pod.
                  More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk

                gitRepo	<Object>
                  gitRepo represents a git repository at a particular revision.
                  DEPRECATED: GitRepo is deprecated. To provision a container with a git repo,
                  mount an
                  EmptyDir into an InitContainer that clones the repo using git, then mount
                  the EmptyDir
                  into the Pod's container.

                glusterfs	<Object>
                  glusterfs represents a Glusterfs mount on the host that shares a pod's
                  lifetime.
                  More info: https://examples.k8s.io/volumes/glusterfs/README.md

                hostPath	<Object>
                  hostPath represents a pre-existing file or directory on the host
                  machine that is directly exposed to the container. This is generally
                  used for system agents or other privileged things that are allowed
                  to see the host machine. Most containers will NOT need this.
                  More info: https://kubernetes.io/docs/concepts/storage/volumes#hostpath
                  ---


                iscsi	<Object>
                  iscsi represents an ISCSI Disk resource that is attached to a
                  kubelet's host machine and then exposed to the pod.
                  More info: https://examples.k8s.io/volumes/iscsi/README.md

                name	<string> -required-
                  name of the volume.
                  Must be a DNS_LABEL and unique within the pod.
                  More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

                nfs	<Object>
                  nfs represents an NFS mount on the host that shares a pod's lifetime
                  More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs

                persistentVolumeClaim	<Object>
                  persistentVolumeClaimVolumeSource represents a reference to a
                  PersistentVolumeClaim in the same namespace.
                  More info:
                  https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims

                photonPersistentDisk	<Object>
                  photonPersistentDisk represents a PhotonController persistent disk attached
                  and mounted on kubelets host machine

                portworxVolume	<Object>
                  portworxVolume represents a portworx volume attached and mounted on kubelets
                  host machine

                projected	<Object>
                  projected items for all in one resources secrets, configmaps, and downward
                  API

                quobyte	<Object>
                  quobyte represents a Quobyte mount on the host that shares a pod's lifetime

                rbd	<Object>
                  rbd represents a Rados Block Device mount on the host that shares a pod's
                  lifetime.
                  More info: https://examples.k8s.io/volumes/rbd/README.md

                scaleIO	<Object>
                  scaleIO represents a ScaleIO persistent volume attached and mounted on
                  Kubernetes nodes.

                secret	<Object>
                  secret represents a secret that should populate this volume.
                  More info: https://kubernetes.io/docs/concepts/storage/volumes#secret

                storageos	<Object>
                  storageOS represents a StorageOS volume attached and mounted on Kubernetes
                  nodes.

                vsphereVolume	<Object>
                  vsphereVolume represents a vSphere volume attached and mounted on kubelets
                  host machine

        """
        super().__init__(**kwargs)

        self.affinity = affinity
        self.args = args
        self.bootstrap_from = bootstrap_from
        self.command = command
        self.connection = connection
        self.database = database
        self.env = env
        self.env_from = env_from
        self.galera = galera
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.inherit_metadata = inherit_metadata
        self.init_containers = init_containers
        self.liveness_probe = liveness_probe
        self.max_scale = max_scale
        self.max_scale_ref = max_scale_ref
        self.metrics = metrics
        self.my_cnf = my_cnf
        self.my_cnf_config_map_key_ref = my_cnf_config_map_key_ref
        self.node_selector = node_selector
        self.password_secret_key_ref = password_secret_key_ref
        self.pod_disruption_budget = pod_disruption_budget
        self.pod_metadata = pod_metadata
        self.pod_security_context = pod_security_context
        self.port = port
        self.primary_connection = primary_connection
        self.primary_service = primary_service
        self.priority_class_name = priority_class_name
        self.readiness_probe = readiness_probe
        self.replicas = replicas
        self.replication = replication
        self.resources = resources
        self.root_empty_password = root_empty_password
        self.root_password_secret_key_ref = root_password_secret_key_ref
        self.secondary_connection = secondary_connection
        self.secondary_service = secondary_service
        self.security_context = security_context
        self.service = service
        self.service_account_name = service_account_name
        self.sidecar_containers = sidecar_containers
        self.storage = storage
        self.tolerations = tolerations
        self.topology_spread_constraints = topology_spread_constraints
        self.update_strategy = update_strategy
        self.username = username
        self.volume_mounts = volume_mounts
        self.volumes = volumes

    def to_dict(self) -> None:
        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.affinity:
                _spec["affinity"] = self.affinity

            if self.args:
                _spec["args"] = self.args

            if self.bootstrap_from:
                _spec["bootstrapFrom"] = self.bootstrap_from

            if self.command:
                _spec["command"] = self.command

            if self.connection:
                _spec["connection"] = self.connection

            if self.database:
                _spec["database"] = self.database

            if self.env:
                _spec["env"] = self.env

            if self.env_from:
                _spec["envFrom"] = self.env_from

            if self.galera:
                _spec["galera"] = self.galera

            if self.image:
                _spec["image"] = self.image

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.image_pull_secrets:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.inherit_metadata:
                _spec["inheritMetadata"] = self.inherit_metadata

            if self.init_containers:
                _spec["initContainers"] = self.init_containers

            if self.liveness_probe:
                _spec["livenessProbe"] = self.liveness_probe

            if self.max_scale:
                _spec["maxScale"] = self.max_scale

            if self.max_scale_ref:
                _spec["maxScaleRef"] = self.max_scale_ref

            if self.metrics:
                _spec["metrics"] = self.metrics

            if self.my_cnf:
                _spec["myCnf"] = self.my_cnf

            if self.my_cnf_config_map_key_ref:
                _spec["myCnfConfigMapKeyRef"] = self.my_cnf_config_map_key_ref

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.password_secret_key_ref:
                _spec["passwordSecretKeyRef"] = self.password_secret_key_ref

            if self.pod_disruption_budget:
                _spec["podDisruptionBudget"] = self.pod_disruption_budget

            if self.pod_metadata:
                _spec["podMetadata"] = self.pod_metadata

            if self.pod_security_context:
                _spec["podSecurityContext"] = self.pod_security_context

            if self.port:
                _spec["port"] = self.port

            if self.primary_connection:
                _spec["primaryConnection"] = self.primary_connection

            if self.primary_service:
                _spec["primaryService"] = self.primary_service

            if self.priority_class_name:
                _spec["priorityClassName"] = self.priority_class_name

            if self.readiness_probe:
                _spec["readinessProbe"] = self.readiness_probe

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.replication:
                _spec["replication"] = self.replication

            if self.resources:
                _spec["resources"] = self.resources

            if self.root_empty_password is not None:
                _spec["rootEmptyPassword"] = self.root_empty_password

            if self.root_password_secret_key_ref:
                _spec["rootPasswordSecretKeyRef"] = self.root_password_secret_key_ref

            if self.secondary_connection:
                _spec["secondaryConnection"] = self.secondary_connection

            if self.secondary_service:
                _spec["secondaryService"] = self.secondary_service

            if self.security_context:
                _spec["securityContext"] = self.security_context

            if self.service:
                _spec["service"] = self.service

            if self.service_account_name:
                _spec["serviceAccountName"] = self.service_account_name

            if self.sidecar_containers:
                _spec["sidecarContainers"] = self.sidecar_containers

            if self.storage:
                _spec["storage"] = self.storage

            if self.tolerations:
                _spec["tolerations"] = self.tolerations

            if self.topology_spread_constraints:
                _spec["topologySpreadConstraints"] = self.topology_spread_constraints

            if self.update_strategy:
                _spec["updateStrategy"] = self.update_strategy

            if self.username:
                _spec["username"] = self.username

            if self.volume_mounts:
                _spec["volumeMounts"] = self.volume_mounts

            if self.volumes:
                _spec["volumes"] = self.volumes
