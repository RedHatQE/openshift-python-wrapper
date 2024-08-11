# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class Prometheus(NamespacedResource):
    """
    Prometheus defines a Prometheus deployment.
    """

    api_group: str = NamespacedResource.ApiGroup.MONITORING_COREOS_COM

    def __init__(
        self,
        additional_alert_manager_configs: Optional[Dict[str, Any]] = None,
        additional_alert_relabel_configs: Optional[Dict[str, Any]] = None,
        additional_args: Optional[List[Any]] = None,
        additional_scrape_configs: Optional[Dict[str, Any]] = None,
        affinity: Optional[Dict[str, Any]] = None,
        alerting: Optional[Dict[str, Any]] = None,
        allow_overlapping_blocks: Optional[bool] = None,
        apiserver_config: Optional[Dict[str, Any]] = None,
        arbitrary_fs_access_through_sms: Optional[Dict[str, Any]] = None,
        base_image: Optional[str] = "",
        body_size_limit: Optional[str] = "",
        config_maps: Optional[Dict[str, Any]] = None,
        containers: Optional[List[Any]] = None,
        disable_compaction: Optional[bool] = None,
        enable_admin_api: Optional[bool] = None,
        enable_features: Optional[Dict[str, Any]] = None,
        enable_remote_write_receiver: Optional[bool] = None,
        enforced_body_size_limit: Optional[str] = "",
        enforced_keep_dropped_targets: Optional[int] = None,
        enforced_label_limit: Optional[int] = None,
        enforced_label_name_length_limit: Optional[int] = None,
        enforced_label_value_length_limit: Optional[int] = None,
        enforced_namespace_label: Optional[str] = "",
        enforced_sample_limit: Optional[int] = None,
        enforced_target_limit: Optional[int] = None,
        evaluation_interval: Optional[str] = "",
        excluded_from_enforcement: Optional[List[Any]] = None,
        exemplars: Optional[Dict[str, Any]] = None,
        external_labels: Optional[Dict[str, Any]] = None,
        external_url: Optional[str] = "",
        host_aliases: Optional[List[Any]] = None,
        host_network: Optional[bool] = None,
        ignore_namespace_selectors: Optional[bool] = None,
        image: Optional[str] = "",
        image_pull_policy: Optional[str] = "",
        image_pull_secrets: Optional[List[Any]] = None,
        init_containers: Optional[List[Any]] = None,
        keep_dropped_targets: Optional[int] = None,
        label_limit: Optional[int] = None,
        label_name_length_limit: Optional[int] = None,
        label_value_length_limit: Optional[int] = None,
        listen_local: Optional[bool] = None,
        log_format: Optional[str] = "",
        log_level: Optional[str] = "",
        maximum_startup_duration_seconds: Optional[int] = None,
        min_ready_seconds: Optional[int] = None,
        node_selector: Optional[Dict[str, Any]] = None,
        override_honor_labels: Optional[bool] = None,
        override_honor_timestamps: Optional[bool] = None,
        paused: Optional[bool] = None,
        persistent_volume_claim_retention_policy: Optional[Dict[str, Any]] = None,
        pod_metadata: Optional[Dict[str, Any]] = None,
        pod_monitor_namespace_selector: Optional[Dict[str, Any]] = None,
        pod_monitor_selector: Optional[Dict[str, Any]] = None,
        pod_target_labels: Optional[Dict[str, Any]] = None,
        port_name: Optional[str] = "",
        priority_class_name: Optional[str] = "",
        probe_namespace_selector: Optional[Dict[str, Any]] = None,
        probe_selector: Optional[Dict[str, Any]] = None,
        prometheus_external_label_name: Optional[str] = "",
        prometheus_rules_excluded_from_enforce: Optional[List[Any]] = None,
        query: Optional[Dict[str, Any]] = None,
        query_log_file: Optional[str] = "",
        reload_strategy: Optional[str] = "",
        remote_read: Optional[List[Any]] = None,
        remote_write: Optional[List[Any]] = None,
        replica_external_label_name: Optional[str] = "",
        replicas: Optional[int] = None,
        resources: Optional[Dict[str, Any]] = None,
        retention: Optional[str] = "",
        retention_size: Optional[str] = "",
        route_prefix: Optional[str] = "",
        rule_namespace_selector: Optional[Dict[str, Any]] = None,
        rule_selector: Optional[Dict[str, Any]] = None,
        rules: Optional[Dict[str, Any]] = None,
        sample_limit: Optional[int] = None,
        scrape_classes: Optional[List[Any]] = None,
        scrape_config_namespace_selector: Optional[Dict[str, Any]] = None,
        scrape_config_selector: Optional[Dict[str, Any]] = None,
        scrape_interval: Optional[str] = "",
        scrape_protocols: Optional[Dict[str, Any]] = None,
        scrape_timeout: Optional[str] = "",
        secrets: Optional[Dict[str, Any]] = None,
        security_context: Optional[Dict[str, Any]] = None,
        service_account_name: Optional[str] = "",
        service_monitor_namespace_selector: Optional[Dict[str, Any]] = None,
        service_monitor_selector: Optional[Dict[str, Any]] = None,
        sha: Optional[str] = "",
        shards: Optional[int] = None,
        storage: Optional[Dict[str, Any]] = None,
        tag: Optional[str] = "",
        target_limit: Optional[int] = None,
        thanos: Optional[Dict[str, Any]] = None,
        tolerations: Optional[List[Any]] = None,
        topology_spread_constraints: Optional[List[Any]] = None,
        tracing_config: Optional[Dict[str, Any]] = None,
        tsdb: Optional[Dict[str, Any]] = None,
        version: Optional[str] = "",
        volume_mounts: Optional[List[Any]] = None,
        volumes: Optional[List[Any]] = None,
        wal_compression: Optional[bool] = None,
        web: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            additional_alert_manager_configs(Dict[Any, Any]): AdditionalAlertManagerConfigs specifies a key of a Secret containing
              additional Prometheus Alertmanager configurations. The Alertmanager
              configurations are appended to the configuration generated by the Prometheus
              Operator. They must be formatted according to the official Prometheus
              documentation:
               https://prometheus.io/docs/prometheus/latest/configuration/configuration/#alertmanager_config
               The user is responsible for making sure that the configurations are valid
               Note that using this feature may expose the possibility to break upgrades
              of Prometheus. It is advised to review Prometheus release notes to ensure
              that no incompatible AlertManager configs are going to break Prometheus
              after the upgrade.

              FIELDS:
                key	<string> -required-
                  The key of the secret to select from.  Must be a valid secret key.

                name	<string>
                  Name of the referent. More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
                  TODO: Add other useful fields. apiVersion, kind, uid?

                optional	<boolean>
                  Specify whether the Secret or its key must be defined

            additional_alert_relabel_configs(Dict[Any, Any]): AdditionalAlertRelabelConfigs specifies a key of a Secret containing
              additional Prometheus alert relabel configurations. The alert relabel
              configurations are appended to the configuration generated by the Prometheus
              Operator. They must be formatted according to the official Prometheus
              documentation:
               https://prometheus.io/docs/prometheus/latest/configuration/configuration/#alert_relabel_configs
               The user is responsible for making sure that the configurations are valid
               Note that using this feature may expose the possibility to break upgrades
              of Prometheus. It is advised to review Prometheus release notes to ensure
              that no incompatible alert relabel configs are going to break Prometheus
              after the upgrade.

              FIELDS:
                key	<string> -required-
                  The key of the secret to select from.  Must be a valid secret key.

                name	<string>
                  Name of the referent. More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
                  TODO: Add other useful fields. apiVersion, kind, uid?

                optional	<boolean>
                  Specify whether the Secret or its key must be defined

            additional_args(List[Any]): AdditionalArgs allows setting additional arguments for the 'prometheus'
              container.
               It is intended for e.g. activating hidden flags which are not supported by
              the dedicated configuration options yet. The arguments are passed as-is to
              the Prometheus container which may cause issues if they are invalid or not
              supported by the given Prometheus version.
               In case of an argument conflict (e.g. an argument which is already set by
              the operator itself) or when providing an invalid argument, the
              reconciliation will fail and an error will be logged.
              Argument as part of the AdditionalArgs list.

              FIELDS:
                name	<string> -required-
                  Name of the argument, e.g. "scrape.discovery-reload-interval".

                value	<string>
                  Argument value, e.g. 30s. Can be empty for name-only arguments (e.g.
                  --storage.tsdb.no-lockfile)

            additional_scrape_configs(Dict[Any, Any]): AdditionalScrapeConfigs allows specifying a key of a Secret containing
              additional Prometheus scrape configurations. Scrape configurations specified
              are appended to the configurations generated by the Prometheus Operator. Job
              configurations specified must have the form as specified in the official
              Prometheus documentation:
              https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config.
              As scrape configs are appended, the user is responsible to make sure it is
              valid. Note that using this feature may expose the possibility to break
              upgrades of Prometheus. It is advised to review Prometheus release notes to
              ensure that no incompatible scrape configs are going to break Prometheus
              after the upgrade.

              FIELDS:
                key	<string> -required-
                  The key of the secret to select from.  Must be a valid secret key.

                name	<string>
                  Name of the referent. More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
                  TODO: Add other useful fields. apiVersion, kind, uid?

                optional	<boolean>
                  Specify whether the Secret or its key must be defined

            affinity(Dict[Any, Any]): Defines the Pods' affinity scheduling rules if specified.

              FIELDS:
                nodeAffinity	<Object>
                  Describes node affinity scheduling rules for the pod.

                podAffinity	<Object>
                  Describes pod affinity scheduling rules (e.g. co-locate this pod in the same
                  node, zone, etc. as some other pod(s)).

                podAntiAffinity	<Object>
                  Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in
                  the same node, zone, etc. as some other pod(s)).

            alerting(Dict[Any, Any]): Defines the settings related to Alertmanager.

              FIELDS:
                alertmanagers	<[]Object> -required-
                  AlertmanagerEndpoints Prometheus should fire alerts against.

            allow_overlapping_blocks(bool): AllowOverlappingBlocks enables vertical compaction and vertical query merge
              in Prometheus.
               Deprecated: this flag has no effect for Prometheus >= 2.39.0 where
              overlapping blocks are enabled by default.

            apiserver_config(Dict[Any, Any]): APIServerConfig allows specifying a host and auth methods to access the
              Kuberntees API server. If null, Prometheus is assumed to run inside of the
              cluster: it will discover the API servers automatically and use the Pod's CA
              certificate and bearer token file at
              /var/run/secrets/kubernetes.io/serviceaccount/.

              FIELDS:
                authorization	<Object>
                  Authorization section for the API server.
                   Cannot be set at the same time as `basicAuth`, `bearerToken`, or
                  `bearerTokenFile`.

                basicAuth	<Object>
                  BasicAuth configuration for the API server.
                   Cannot be set at the same time as `authorization`, `bearerToken`, or
                  `bearerTokenFile`.

                bearerToken	<string>
                  *Warning: this field shouldn't be used because the token value appears in
                  clear-text. Prefer using `authorization`.*
                   Deprecated: this will be removed in a future release.

                bearerTokenFile	<string>
                  File to read bearer token for accessing apiserver.
                   Cannot be set at the same time as `basicAuth`, `authorization`, or
                  `bearerToken`.
                   Deprecated: this will be removed in a future release. Prefer using
                  `authorization`.

                host	<string> -required-
                  Kubernetes API address consisting of a hostname or IP address followed by an
                  optional port number.

                tlsConfig	<Object>
                  TLS Config to use for the API server.

            arbitrary_fs_access_through_sms(Dict[Any, Any]): When true, ServiceMonitor, PodMonitor and Probe object are forbidden to
              reference arbitrary files on the file system of the 'prometheus' container.
              When a ServiceMonitor's endpoint specifies a `bearerTokenFile` value (e.g.
              '/var/run/secrets/kubernetes.io/serviceaccount/token'), a malicious target
              can get access to the Prometheus service account's token in the Prometheus'
              scrape request. Setting `spec.arbitraryFSAccessThroughSM` to 'true' would
              prevent the attack. Users should instead provide the credentials using the
              `spec.bearerTokenSecret` field.

              FIELDS:
                deny	<boolean>
                  <no description>

            base_image(str): Deprecated: use 'spec.image' instead.

            body_size_limit(str): BodySizeLimit defines per-scrape on response body size. Only valid in
              Prometheus versions 2.45.0 and newer.

            config_maps(Dict[Any, Any]): ConfigMaps is a list of ConfigMaps in the same namespace as the Prometheus
              object, which shall be mounted into the Prometheus Pods. Each ConfigMap is
              added to the StatefulSet definition as a volume named
              `configmap-<configmap-name>`. The ConfigMaps are mounted into
              /etc/prometheus/configmaps/<configmap-name> in the 'prometheus' container.

            containers(List[Any]): Containers allows injecting additional containers or modifying operator
              generated containers. This can be used to allow adding an authentication
              proxy to the Pods or to change the behavior of an operator generated
              container. Containers described here modify an operator generated container
              if they share the same name and modifications are done via a strategic merge
              patch.
               The names of containers managed by the operator are: * `prometheus` *
              `config-reloader` * `thanos-sidecar`
               Overriding containers is entirely outside the scope of what the maintainers
              will support and by doing so, you accept that this behaviour may break at
              any time without notice.
              A single application container that you want to run within a pod.

              FIELDS:
                args	<[]string>
                  Arguments to the entrypoint. The container image's CMD is used if this is
                  not provided. Variable references $(VAR_NAME) are expanded using the
                  container's environment. If a variable cannot be resolved, the reference in
                  the input string will be unchanged. Double $$ are reduced to a single $,
                  which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will
                  produce the string literal "$(VAR_NAME)". Escaped references will never be
                  expanded, regardless of whether the variable exists or not. Cannot be
                  updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                command	<[]string>
                  Entrypoint array. Not executed within a shell. The container image's
                  ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME)
                  are expanded using the container's environment. If a variable cannot be
                  resolved, the reference in the input string will be unchanged. Double $$ are
                  reduced to a single $, which allows for escaping the $(VAR_NAME) syntax:
                  i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped
                  references will never be expanded, regardless of whether the variable exists
                  or not. Cannot be updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                env	<[]Object>
                  List of environment variables to set in the container. Cannot be updated.

                envFrom	<[]Object>
                  List of sources to populate environment variables in the container. The keys
                  defined within a source must be a C_IDENTIFIER. All invalid keys will be
                  reported as an event when the container is starting. When a key exists in
                  multiple sources, the value associated with the last source will take
                  precedence. Values defined by an Env with a duplicate key will take
                  precedence. Cannot be updated.

                image	<string>
                  Container image name. More info:
                  https://kubernetes.io/docs/concepts/containers/images This field is optional
                  to allow higher level config management to default or override container
                  images in workload controllers like Deployments and StatefulSets.

                imagePullPolicy	<string>
                  Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if
                  :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More
                  info: https://kubernetes.io/docs/concepts/containers/images#updating-images

                lifecycle	<Object>
                  Actions that the management system should take in response to container
                  lifecycle events. Cannot be updated.

                livenessProbe	<Object>
                  Periodic probe of container liveness. Container will be restarted if the
                  probe fails. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                name	<string> -required-
                  Name of the container specified as a DNS_LABEL. Each container in a pod must
                  have a unique name (DNS_LABEL). Cannot be updated.

                ports	<[]Object>
                  List of ports to expose from the container. Not specifying a port here DOES
                  NOT prevent that port from being exposed. Any port which is listening on the
                  default "0.0.0.0" address inside a container will be accessible from the
                  network. Modifying this array with strategic merge patch may corrupt the
                  data. For more information See
                  https://github.com/kubernetes/kubernetes/issues/108255. Cannot be updated.

                readinessProbe	<Object>
                  Periodic probe of container service readiness. Container will be removed
                  from service endpoints if the probe fails. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                resizePolicy	<[]Object>
                  Resources resize policy for the container.

                resources	<Object>
                  Compute Resources required by this container. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

                restartPolicy	<string>
                  RestartPolicy defines the restart behavior of individual containers in a
                  pod. This field may only be set for init containers, and the only allowed
                  value is "Always". For non-init containers or when this field is not
                  specified, the restart behavior is defined by the Pod's restart policy and
                  the container type. Setting the RestartPolicy as "Always" for the init
                  container will have the following effect: this init container will be
                  continually restarted on exit until all regular containers have terminated.
                  Once all regular containers have completed, all init containers with
                  restartPolicy "Always" will be shut down. This lifecycle differs from normal
                  init containers and is often referred to as a "sidecar" container. Although
                  this init container still starts in the init container sequence, it does not
                  wait for the container to complete before proceeding to the next init
                  container. Instead, the next init container starts immediately after this
                  init container is started, or after any startupProbe has successfully
                  completed.

                securityContext	<Object>
                  SecurityContext defines the security options the container should be run
                  with. If set, the fields of SecurityContext override the equivalent fields
                  of PodSecurityContext. More info:
                  https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

                startupProbe	<Object>
                  StartupProbe indicates that the Pod has successfully initialized. If
                  specified, no other probes are executed until this completes successfully.
                  If this probe fails, the Pod will be restarted, just as if the livenessProbe
                  failed. This can be used to provide different probe parameters at the
                  beginning of a Pod's lifecycle, when it might take a long time to load data
                  or warm a cache, than during steady-state operation. This cannot be updated.
                  More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                stdin	<boolean>
                  Whether this container should allocate a buffer for stdin in the container
                  runtime. If this is not set, reads from stdin in the container will always
                  result in EOF. Default is false.

                stdinOnce	<boolean>
                  Whether the container runtime should close the stdin channel after it has
                  been opened by a single attach. When stdin is true the stdin stream will
                  remain open across multiple attach sessions. If stdinOnce is set to true,
                  stdin is opened on container start, is empty until the first client attaches
                  to stdin, and then remains open and accepts data until the client
                  disconnects, at which time stdin is closed and remains closed until the
                  container is restarted. If this flag is false, a container processes that
                  reads from stdin will never receive an EOF. Default is false

                terminationMessagePath	<string>
                  Optional: Path at which the file to which the container's termination
                  message will be written is mounted into the container's filesystem. Message
                  written is intended to be brief final status, such as an assertion failure
                  message. Will be truncated by the node if greater than 4096 bytes. The total
                  message length across all containers will be limited to 12kb. Defaults to
                  /dev/termination-log. Cannot be updated.

                terminationMessagePolicy	<string>
                  Indicate how the termination message should be populated. File will use the
                  contents of terminationMessagePath to populate the container status message
                  on both success and failure. FallbackToLogsOnError will use the last chunk
                  of container log output if the termination message file is empty and the
                  container exited with an error. The log output is limited to 2048 bytes or
                  80 lines, whichever is smaller. Defaults to File. Cannot be updated.

                tty	<boolean>
                  Whether this container should allocate a TTY for itself, also requires
                  'stdin' to be true. Default is false.

                volumeDevices	<[]Object>
                  volumeDevices is the list of block devices to be used by the container.

                volumeMounts	<[]Object>
                  Pod volumes to mount into the container's filesystem. Cannot be updated.

                workingDir	<string>
                  Container's working directory. If not specified, the container runtime's
                  default will be used, which might be configured in the container image.
                  Cannot be updated.

            disable_compaction(bool): When true, the Prometheus compaction is disabled.

            enable_admin_api(bool): Enables access to the Prometheus web admin API.
               WARNING: Enabling the admin APIs enables mutating endpoints, to delete
              data, shutdown Prometheus, and more. Enabling this should be done with care
              and the user is advised to add additional authentication authorization via a
              proxy to ensure only clients authorized to perform these actions can do so.
               For more information:
              https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-admin-apis

            enable_features(Dict[Any, Any]): Enable access to Prometheus feature flags. By default, no features are
              enabled.
               Enabling features which are disabled by default is entirely outside the
              scope of what the maintainers will support and by doing so, you accept that
              this behaviour may break at any time without notice.
               For more information see
              https://prometheus.io/docs/prometheus/latest/feature_flags/

            enable_remote_write_receiver(bool): Enable Prometheus to be used as a receiver for the Prometheus remote write
              protocol.
               WARNING: This is not considered an efficient way of ingesting samples. Use
              it with caution for specific low-volume use cases. It is not suitable for
              replacing the ingestion via scraping and turning Prometheus into a
              push-based metrics collection system. For more information see
              https://prometheus.io/docs/prometheus/latest/querying/api/#remote-write-receiver
               It requires Prometheus >= v2.33.0.

            enforced_body_size_limit(str): When defined, enforcedBodySizeLimit specifies a global limit on the size of
              uncompressed response body that will be accepted by Prometheus. Targets
              responding with a body larger than this many bytes will cause the scrape to
              fail.
               It requires Prometheus >= v2.28.0.

            enforced_keep_dropped_targets(int): When defined, enforcedKeepDroppedTargets specifies a global limit on the
              number of targets dropped by relabeling that will be kept in memory. The
              value overrides any `spec.keepDroppedTargets` set by ServiceMonitor,
              PodMonitor, Probe objects unless `spec.keepDroppedTargets` is greater than
              zero and less than `spec.enforcedKeepDroppedTargets`.
               It requires Prometheus >= v2.47.0.

            enforced_label_limit(int): When defined, enforcedLabelLimit specifies a global limit on the number of
              labels per sample. The value overrides any `spec.labelLimit` set by
              ServiceMonitor, PodMonitor, Probe objects unless `spec.labelLimit` is
              greater than zero and less than `spec.enforcedLabelLimit`.
               It requires Prometheus >= v2.27.0.

            enforced_label_name_length_limit(int): When defined, enforcedLabelNameLengthLimit specifies a global limit on the
              length of labels name per sample. The value overrides any
              `spec.labelNameLengthLimit` set by ServiceMonitor, PodMonitor, Probe objects
              unless `spec.labelNameLengthLimit` is greater than zero and less than
              `spec.enforcedLabelNameLengthLimit`.
               It requires Prometheus >= v2.27.0.

            enforced_label_value_length_limit(int): When not null, enforcedLabelValueLengthLimit defines a global limit on the
              length of labels value per sample. The value overrides any
              `spec.labelValueLengthLimit` set by ServiceMonitor, PodMonitor, Probe
              objects unless `spec.labelValueLengthLimit` is greater than zero and less
              than `spec.enforcedLabelValueLengthLimit`.
               It requires Prometheus >= v2.27.0.

            enforced_namespace_label(str): When not empty, a label will be added to
               1. All metrics scraped from `ServiceMonitor`, `PodMonitor`, `Probe` and
              `ScrapeConfig` objects. 2. All metrics generated from recording rules
              defined in `PrometheusRule` objects. 3. All alerts generated from alerting
              rules defined in `PrometheusRule` objects. 4. All vector selectors of PromQL
              expressions defined in `PrometheusRule` objects.
               The label will not added for objects referenced in
              `spec.excludedFromEnforcement`.
               The label's name is this field's value. The label's value is the namespace
              of the `ServiceMonitor`, `PodMonitor`, `Probe` or `PrometheusRule` object.

            enforced_sample_limit(int): When defined, enforcedSampleLimit specifies a global limit on the number of
              scraped samples that will be accepted. This overrides any `spec.sampleLimit`
              set by ServiceMonitor, PodMonitor, Probe objects unless `spec.sampleLimit`
              is greater than zero and less than `spec.enforcedSampleLimit`.
               It is meant to be used by admins to keep the overall number of
              samples/series under a desired limit.

            enforced_target_limit(int): When defined, enforcedTargetLimit specifies a global limit on the number of
              scraped targets. The value overrides any `spec.targetLimit` set by
              ServiceMonitor, PodMonitor, Probe objects unless `spec.targetLimit` is
              greater than zero and less than `spec.enforcedTargetLimit`.
               It is meant to be used by admins to to keep the overall number of targets
              under a desired limit.

            evaluation_interval(str): Interval between rule evaluations. Default: "30s"

            excluded_from_enforcement(List[Any]): List of references to PodMonitor, ServiceMonitor, Probe and PrometheusRule
              objects to be excluded from enforcing a namespace label of origin.
               It is only applicable if `spec.enforcedNamespaceLabel` set to true.
              ObjectReference references a PodMonitor, ServiceMonitor, Probe or
              PrometheusRule object.

              FIELDS:
                group	<string>
                  Group of the referent. When not specified, it defaults to
                  `monitoring.coreos.com`

                name	<string>
                  Name of the referent. When not set, all resources in the namespace are
                  matched.

                namespace	<string> -required-
                  Namespace of the referent. More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/

                resource	<string> -required-
                  Resource of the referent.

            exemplars(Dict[Any, Any]): Exemplars related settings that are runtime reloadable. It requires to
              enable the `exemplar-storage` feature flag to be effective.

              FIELDS:
                maxSize	<integer>
                  Maximum number of exemplars stored in memory for all series.
                   exemplar-storage itself must be enabled using the `spec.enableFeature`
                  option for exemplars to be scraped in the first place.
                   If not set, Prometheus uses its default value. A value of zero or less than
                  zero disables the storage.

            external_labels(Dict[Any, Any]): The labels to add to any time series or alerts when communicating with
              external systems (federation, remote storage, Alertmanager). Labels defined
              by `spec.replicaExternalLabelName` and `spec.prometheusExternalLabelName`
              take precedence over this list.

            external_url(str): The external URL under which the Prometheus service is externally available.
              This is necessary to generate correct URLs (for instance if Prometheus is
              accessible behind an Ingress resource).

            host_aliases(List[Any]): Optional list of hosts and IPs that will be injected into the Pod's hosts
              file if specified.
              HostAlias holds the mapping between IP and hostnames that will be injected
              as an entry in the pod's hosts file.

              FIELDS:
                hostnames	<[]string> -required-
                  Hostnames for the above IP address.

                ip	<string> -required-
                  IP address of the host file entry.

            host_network(bool): Use the host's network namespace if true.
               Make sure to understand the security implications if you want to enable it
              (https://kubernetes.io/docs/concepts/configuration/overview/).
               When hostNetwork is enabled, this will set the DNS policy to
              `ClusterFirstWithHostNet` automatically.

            ignore_namespace_selectors(bool): When true, `spec.namespaceSelector` from all PodMonitor, ServiceMonitor and
              Probe objects will be ignored. They will only discover targets within the
              namespace of the PodMonitor, ServiceMonitor and Probe object.

            image(str): Container image name for Prometheus. If specified, it takes precedence over
              the `spec.baseImage`, `spec.tag` and `spec.sha` fields.
               Specifying `spec.version` is still necessary to ensure the Prometheus
              Operator knows which version of Prometheus is being configured.
               If neither `spec.image` nor `spec.baseImage` are defined, the operator will
              use the latest upstream version of Prometheus available at the time when the
              operator was released.

            image_pull_policy(str): Image pull policy for the 'prometheus', 'init-config-reloader' and
              'config-reloader' containers. See
              https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy for
              more details.

            image_pull_secrets(List[Any]): An optional list of references to Secrets in the same namespace to use for
              pulling images from registries. See
              http://kubernetes.io/docs/user-guide/images#specifying-imagepullsecrets-on-a-pod
              LocalObjectReference contains enough information to let you locate the
              referenced object inside the same namespace.

              FIELDS:
                name	<string>
                  Name of the referent. More info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
                  TODO: Add other useful fields. apiVersion, kind, uid?

            init_containers(List[Any]): InitContainers allows injecting initContainers to the Pod definition. Those
              can be used to e.g.  fetch secrets for injection into the Prometheus
              configuration from external sources. Any errors during the execution of an
              initContainer will lead to a restart of the Pod. More info:
              https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
              InitContainers described here modify an operator generated init containers
              if they share the same name and modifications are done via a strategic merge
              patch.
               The names of init container name managed by the operator are: *
              `init-config-reloader`.
               Overriding init containers is entirely outside the scope of what the
              maintainers will support and by doing so, you accept that this behaviour may
              break at any time without notice.
              A single application container that you want to run within a pod.

              FIELDS:
                args	<[]string>
                  Arguments to the entrypoint. The container image's CMD is used if this is
                  not provided. Variable references $(VAR_NAME) are expanded using the
                  container's environment. If a variable cannot be resolved, the reference in
                  the input string will be unchanged. Double $$ are reduced to a single $,
                  which allows for escaping the $(VAR_NAME) syntax: i.e. "$$(VAR_NAME)" will
                  produce the string literal "$(VAR_NAME)". Escaped references will never be
                  expanded, regardless of whether the variable exists or not. Cannot be
                  updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                command	<[]string>
                  Entrypoint array. Not executed within a shell. The container image's
                  ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME)
                  are expanded using the container's environment. If a variable cannot be
                  resolved, the reference in the input string will be unchanged. Double $$ are
                  reduced to a single $, which allows for escaping the $(VAR_NAME) syntax:
                  i.e. "$$(VAR_NAME)" will produce the string literal "$(VAR_NAME)". Escaped
                  references will never be expanded, regardless of whether the variable exists
                  or not. Cannot be updated. More info:
                  https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

                env	<[]Object>
                  List of environment variables to set in the container. Cannot be updated.

                envFrom	<[]Object>
                  List of sources to populate environment variables in the container. The keys
                  defined within a source must be a C_IDENTIFIER. All invalid keys will be
                  reported as an event when the container is starting. When a key exists in
                  multiple sources, the value associated with the last source will take
                  precedence. Values defined by an Env with a duplicate key will take
                  precedence. Cannot be updated.

                image	<string>
                  Container image name. More info:
                  https://kubernetes.io/docs/concepts/containers/images This field is optional
                  to allow higher level config management to default or override container
                  images in workload controllers like Deployments and StatefulSets.

                imagePullPolicy	<string>
                  Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always if
                  :latest tag is specified, or IfNotPresent otherwise. Cannot be updated. More
                  info: https://kubernetes.io/docs/concepts/containers/images#updating-images

                lifecycle	<Object>
                  Actions that the management system should take in response to container
                  lifecycle events. Cannot be updated.

                livenessProbe	<Object>
                  Periodic probe of container liveness. Container will be restarted if the
                  probe fails. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                name	<string> -required-
                  Name of the container specified as a DNS_LABEL. Each container in a pod must
                  have a unique name (DNS_LABEL). Cannot be updated.

                ports	<[]Object>
                  List of ports to expose from the container. Not specifying a port here DOES
                  NOT prevent that port from being exposed. Any port which is listening on the
                  default "0.0.0.0" address inside a container will be accessible from the
                  network. Modifying this array with strategic merge patch may corrupt the
                  data. For more information See
                  https://github.com/kubernetes/kubernetes/issues/108255. Cannot be updated.

                readinessProbe	<Object>
                  Periodic probe of container service readiness. Container will be removed
                  from service endpoints if the probe fails. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                resizePolicy	<[]Object>
                  Resources resize policy for the container.

                resources	<Object>
                  Compute Resources required by this container. Cannot be updated. More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

                restartPolicy	<string>
                  RestartPolicy defines the restart behavior of individual containers in a
                  pod. This field may only be set for init containers, and the only allowed
                  value is "Always". For non-init containers or when this field is not
                  specified, the restart behavior is defined by the Pod's restart policy and
                  the container type. Setting the RestartPolicy as "Always" for the init
                  container will have the following effect: this init container will be
                  continually restarted on exit until all regular containers have terminated.
                  Once all regular containers have completed, all init containers with
                  restartPolicy "Always" will be shut down. This lifecycle differs from normal
                  init containers and is often referred to as a "sidecar" container. Although
                  this init container still starts in the init container sequence, it does not
                  wait for the container to complete before proceeding to the next init
                  container. Instead, the next init container starts immediately after this
                  init container is started, or after any startupProbe has successfully
                  completed.

                securityContext	<Object>
                  SecurityContext defines the security options the container should be run
                  with. If set, the fields of SecurityContext override the equivalent fields
                  of PodSecurityContext. More info:
                  https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

                startupProbe	<Object>
                  StartupProbe indicates that the Pod has successfully initialized. If
                  specified, no other probes are executed until this completes successfully.
                  If this probe fails, the Pod will be restarted, just as if the livenessProbe
                  failed. This can be used to provide different probe parameters at the
                  beginning of a Pod's lifecycle, when it might take a long time to load data
                  or warm a cache, than during steady-state operation. This cannot be updated.
                  More info:
                  https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

                stdin	<boolean>
                  Whether this container should allocate a buffer for stdin in the container
                  runtime. If this is not set, reads from stdin in the container will always
                  result in EOF. Default is false.

                stdinOnce	<boolean>
                  Whether the container runtime should close the stdin channel after it has
                  been opened by a single attach. When stdin is true the stdin stream will
                  remain open across multiple attach sessions. If stdinOnce is set to true,
                  stdin is opened on container start, is empty until the first client attaches
                  to stdin, and then remains open and accepts data until the client
                  disconnects, at which time stdin is closed and remains closed until the
                  container is restarted. If this flag is false, a container processes that
                  reads from stdin will never receive an EOF. Default is false

                terminationMessagePath	<string>
                  Optional: Path at which the file to which the container's termination
                  message will be written is mounted into the container's filesystem. Message
                  written is intended to be brief final status, such as an assertion failure
                  message. Will be truncated by the node if greater than 4096 bytes. The total
                  message length across all containers will be limited to 12kb. Defaults to
                  /dev/termination-log. Cannot be updated.

                terminationMessagePolicy	<string>
                  Indicate how the termination message should be populated. File will use the
                  contents of terminationMessagePath to populate the container status message
                  on both success and failure. FallbackToLogsOnError will use the last chunk
                  of container log output if the termination message file is empty and the
                  container exited with an error. The log output is limited to 2048 bytes or
                  80 lines, whichever is smaller. Defaults to File. Cannot be updated.

                tty	<boolean>
                  Whether this container should allocate a TTY for itself, also requires
                  'stdin' to be true. Default is false.

                volumeDevices	<[]Object>
                  volumeDevices is the list of block devices to be used by the container.

                volumeMounts	<[]Object>
                  Pod volumes to mount into the container's filesystem. Cannot be updated.

                workingDir	<string>
                  Container's working directory. If not specified, the container runtime's
                  default will be used, which might be configured in the container image.
                  Cannot be updated.

            keep_dropped_targets(int): Per-scrape limit on the number of targets dropped by relabeling that will be
              kept in memory. 0 means no limit.
               It requires Prometheus >= v2.47.0.

            label_limit(int): Per-scrape limit on number of labels that will be accepted for a sample.
              Only valid in Prometheus versions 2.45.0 and newer.

            label_name_length_limit(int): Per-scrape limit on length of labels name that will be accepted for a
              sample. Only valid in Prometheus versions 2.45.0 and newer.

            label_value_length_limit(int): Per-scrape limit on length of labels value that will be accepted for a
              sample. Only valid in Prometheus versions 2.45.0 and newer.

            listen_local(bool): When true, the Prometheus server listens on the loopback address instead of
              the Pod IP's address.

            log_format(str): Log format for Log level for Prometheus and the config-reloader sidecar.

            log_level(str): Log level for Prometheus and the config-reloader sidecar.

            maximum_startup_duration_seconds(int): Defines the maximum time that the `prometheus` container's startup probe
              will wait before being considered failed. The startup probe will return
              success after the WAL replay is complete. If set, the value should be
              greater than 60 (seconds). Otherwise it will be equal to 600 seconds (15
              minutes).

            min_ready_seconds(int): Minimum number of seconds for which a newly created Pod should be ready
              without any of its container crashing for it to be considered available.
              Defaults to 0 (pod will be considered available as soon as it is ready)
               This is an alpha field from kubernetes 1.22 until 1.24 which requires
              enabling the StatefulSetMinReadySeconds feature gate.

            node_selector(Dict[Any, Any]): Defines on which Nodes the Pods are scheduled.

            override_honor_labels(bool): When true, Prometheus resolves label conflicts by renaming the labels in the
              scraped data to "exported_<label value>" for all targets created from
              service and pod monitors. Otherwise the HonorLabels field of the service or
              pod monitor applies.

            override_honor_timestamps(bool): When true, Prometheus ignores the timestamps for all the targets created
              from service and pod monitors. Otherwise the HonorTimestamps field of the
              service or pod monitor applies.

            paused(bool): When a Prometheus deployment is paused, no actions except for deletion will
              be performed on the underlying objects.

            persistent_volume_claim_retention_policy(Dict[Any, Any]): The field controls if and how PVCs are deleted during the lifecycle of a
              StatefulSet. The default behavior is all PVCs are retained. This is an alpha
              field from kubernetes 1.23 until 1.26 and a beta field from 1.26. It
              requires enabling the StatefulSetAutoDeletePVC feature gate.

              FIELDS:
                whenDeleted	<string>
                  WhenDeleted specifies what happens to PVCs created from StatefulSet
                  VolumeClaimTemplates when the StatefulSet is deleted. The default policy of
                  `Retain` causes PVCs to not be affected by StatefulSet deletion. The
                  `Delete` policy causes those PVCs to be deleted.

                whenScaled	<string>
                  WhenScaled specifies what happens to PVCs created from StatefulSet
                  VolumeClaimTemplates when the StatefulSet is scaled down. The default policy
                  of `Retain` causes PVCs to not be affected by a scaledown. The `Delete`
                  policy causes the associated PVCs for any excess pods above the replica
                  count to be deleted.

            pod_metadata(Dict[Any, Any]): PodMetadata configures labels and annotations which are propagated to the
              Prometheus pods.
               The following items are reserved and cannot be overridden: * "prometheus"
              label, set to the name of the Prometheus object. *
              "app.kubernetes.io/instance" label, set to the name of the Prometheus
              object. * "app.kubernetes.io/managed-by" label, set to
              "prometheus-operator". * "app.kubernetes.io/name" label, set to
              "prometheus". * "app.kubernetes.io/version" label, set to the Prometheus
              version. * "operator.prometheus.io/name" label, set to the name of the
              Prometheus object. * "operator.prometheus.io/shard" label, set to the shard
              number of the Prometheus object. * "kubectl.kubernetes.io/default-container"
              annotation, set to "prometheus".

              FIELDS:
                annotations	<map[string]string>
                  Annotations is an unstructured key value map stored with a resource that may
                  be set by external tools to store and retrieve arbitrary metadata. They are
                  not queryable and should be preserved when modifying objects. More info:
                  http://kubernetes.io/docs/user-guide/annotations

                labels	<map[string]string>
                  Map of string keys and values that can be used to organize and categorize
                  (scope and select) objects. May match selectors of replication controllers
                  and services. More info: http://kubernetes.io/docs/user-guide/labels

                name	<string>
                  Name must be unique within a namespace. Is required when creating resources,
                  although some resources may allow a client to request the generation of an
                  appropriate name automatically. Name is primarily intended for creation
                  idempotence and configuration definition. Cannot be updated. More info:
                  http://kubernetes.io/docs/user-guide/identifiers#names

            pod_monitor_namespace_selector(Dict[Any, Any]): Namespaces to match for PodMonitors discovery. An empty label selector
              matches all namespaces. A null label selector matches the current namespace
              only.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            pod_monitor_selector(Dict[Any, Any]): PodMonitors to be selected for target discovery. An empty label selector
              matches all objects. A null label selector matches no objects.
               If `spec.serviceMonitorSelector`, `spec.podMonitorSelector`,
              `spec.probeSelector` and `spec.scrapeConfigSelector` are null, the
              Prometheus configuration is unmanaged. The Prometheus operator will ensure
              that the Prometheus configuration's Secret exists, but it is the
              responsibility of the user to provide the raw gzipped Prometheus
              configuration under the `prometheus.yaml.gz` key. This behavior is
              *deprecated* and will be removed in the next major version of the custom
              resource definition. It is recommended to use `spec.additionalScrapeConfigs`
              instead.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            pod_target_labels(Dict[Any, Any]): PodTargetLabels are appended to the `spec.podTargetLabels` field of all
              PodMonitor and ServiceMonitor objects.

            port_name(str): Port name used for the pods and governing service. Default: "web"

            priority_class_name(str): Priority class assigned to the Pods.

            probe_namespace_selector(Dict[Any, Any]): Namespaces to match for Probe discovery. An empty label selector matches all
              namespaces. A null label selector matches the current namespace only.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            probe_selector(Dict[Any, Any]): Probes to be selected for target discovery. An empty label selector matches
              all objects. A null label selector matches no objects.
               If `spec.serviceMonitorSelector`, `spec.podMonitorSelector`,
              `spec.probeSelector` and `spec.scrapeConfigSelector` are null, the
              Prometheus configuration is unmanaged. The Prometheus operator will ensure
              that the Prometheus configuration's Secret exists, but it is the
              responsibility of the user to provide the raw gzipped Prometheus
              configuration under the `prometheus.yaml.gz` key. This behavior is
              *deprecated* and will be removed in the next major version of the custom
              resource definition. It is recommended to use `spec.additionalScrapeConfigs`
              instead.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            prometheus_external_label_name(str): Name of Prometheus external label used to denote the Prometheus instance
              name. The external label will _not_ be added when the field is set to the
              empty string (`""`).
               Default: "prometheus"

            prometheus_rules_excluded_from_enforce(List[Any]): Defines the list of PrometheusRule objects to which the namespace label
              enforcement doesn't apply. This is only relevant when
              `spec.enforcedNamespaceLabel` is set to true. Deprecated: use
              `spec.excludedFromEnforcement` instead.
              PrometheusRuleExcludeConfig enables users to configure excluded
              PrometheusRule names and their namespaces to be ignored while enforcing
              namespace label for alerts and metrics.

              FIELDS:
                ruleName	<string> -required-
                  Name of the excluded PrometheusRule object.

                ruleNamespace	<string> -required-
                  Namespace of the excluded PrometheusRule object.

            query(Dict[Any, Any]): QuerySpec defines the configuration of the Promethus query service.

              FIELDS:
                lookbackDelta	<string>
                  The delta difference allowed for retrieving metrics during expression
                  evaluations.

                maxConcurrency	<integer>
                  Number of concurrent queries that can be run at once.

                maxSamples	<integer>
                  Maximum number of samples a single query can load into memory. Note that
                  queries will fail if they would load more samples than this into memory, so
                  this also limits the number of samples a query can return.

                timeout	<string>
                  Maximum time a query may take before being aborted.

            query_log_file(str): queryLogFile specifies where the file to which PromQL queries are logged.
               If the filename has an empty path, e.g. 'query.log', The Prometheus Pods
              will mount the file into an emptyDir volume at `/var/log/prometheus`. If a
              full path is provided, e.g. '/var/log/prometheus/query.log', you must mount
              a volume in the specified directory and it must be writable. This is because
              the prometheus container runs with a read-only root filesystem for security
              reasons. Alternatively, the location can be set to a standard I/O stream,
              e.g. `/dev/stdout`, to log query information to the default Prometheus log
              stream.

            reload_strategy(str): Defines the strategy used to reload the Prometheus configuration. If not
              specified, the configuration is reloaded using the /-/reload HTTP endpoint.

            remote_read(List[Any]): Defines the list of remote read configurations.
              RemoteReadSpec defines the configuration for Prometheus to read back samples
              from a remote endpoint.

              FIELDS:
                authorization	<Object>
                  Authorization section for the URL.
                   It requires Prometheus >= v2.26.0.
                   Cannot be set at the same time as `basicAuth`, or `oauth2`.

                basicAuth	<Object>
                  BasicAuth configuration for the URL.
                   Cannot be set at the same time as `authorization`, or `oauth2`.

                bearerToken	<string>
                  *Warning: this field shouldn't be used because the token value appears in
                  clear-text. Prefer using `authorization`.*
                   Deprecated: this will be removed in a future release.

                bearerTokenFile	<string>
                  File from which to read the bearer token for the URL.
                   Deprecated: this will be removed in a future release. Prefer using
                  `authorization`.

                filterExternalLabels	<boolean>
                  Whether to use the external labels as selectors for the remote read
                  endpoint.
                   It requires Prometheus >= v2.34.0.

                followRedirects	<boolean>
                  Configure whether HTTP requests follow HTTP 3xx redirects.
                   It requires Prometheus >= v2.26.0.

                headers	<map[string]string>
                  Custom HTTP headers to be sent along with each remote read request. Be aware
                  that headers that are set by Prometheus itself can't be overwritten. Only
                  valid in Prometheus versions 2.26.0 and newer.

                name	<string>
                  The name of the remote read queue, it must be unique if specified. The name
                  is used in metrics and logging in order to differentiate read
                  configurations.
                   It requires Prometheus >= v2.15.0.

                oauth2	<Object>
                  OAuth2 configuration for the URL.
                   It requires Prometheus >= v2.27.0.
                   Cannot be set at the same time as `authorization`, or `basicAuth`.

                proxyUrl	<string>
                  Optional ProxyURL.

                readRecent	<boolean>
                  Whether reads should be made for queries for time ranges that the local
                  storage should have complete data for.

                remoteTimeout	<string>
                  Timeout for requests to the remote read endpoint.

                requiredMatchers	<map[string]string>
                  An optional list of equality matchers which have to be present in a selector
                  to query the remote read endpoint.

                tlsConfig	<Object>
                  TLS Config to use for the URL.

                url	<string> -required-
                  The URL of the endpoint to query from.

            remote_write(List[Any]): Defines the list of remote write configurations.
              RemoteWriteSpec defines the configuration to write samples from Prometheus
              to a remote endpoint.

              FIELDS:
                authorization	<Object>
                  Authorization section for the URL.
                   It requires Prometheus >= v2.26.0.
                   Cannot be set at the same time as `sigv4`, `basicAuth`, `oauth2`, or
                  `azureAd`.

                azureAd	<Object>
                  AzureAD for the URL.
                   It requires Prometheus >= v2.45.0.
                   Cannot be set at the same time as `authorization`, `basicAuth`, `oauth2`,
                  or `sigv4`.

                basicAuth	<Object>
                  BasicAuth configuration for the URL.
                   Cannot be set at the same time as `sigv4`, `authorization`, `oauth2`, or
                  `azureAd`.

                bearerToken	<string>
                  *Warning: this field shouldn't be used because the token value appears in
                  clear-text. Prefer using `authorization`.*
                   Deprecated: this will be removed in a future release.

                bearerTokenFile	<string>
                  File from which to read bearer token for the URL.
                   Deprecated: this will be removed in a future release. Prefer using
                  `authorization`.

                enableHTTP2	<boolean>
                  Whether to enable HTTP2.

                headers	<map[string]string>
                  Custom HTTP headers to be sent along with each remote write request. Be
                  aware that headers that are set by Prometheus itself can't be overwritten.
                   It requires Prometheus >= v2.25.0.

                metadataConfig	<Object>
                  MetadataConfig configures the sending of series metadata to the remote
                  storage.

                name	<string>
                  The name of the remote write queue, it must be unique if specified. The name
                  is used in metrics and logging in order to differentiate queues.
                   It requires Prometheus >= v2.15.0.

                oauth2	<Object>
                  OAuth2 configuration for the URL.
                   It requires Prometheus >= v2.27.0.
                   Cannot be set at the same time as `sigv4`, `authorization`, `basicAuth`, or
                  `azureAd`.

                proxyUrl	<string>
                  Optional ProxyURL.

                queueConfig	<Object>
                  QueueConfig allows tuning of the remote write queue parameters.

                remoteTimeout	<string>
                  Timeout for requests to the remote write endpoint.

                sendExemplars	<boolean>
                  Enables sending of exemplars over remote write. Note that exemplar-storage
                  itself must be enabled using the `spec.enableFeature` option for exemplars
                  to be scraped in the first place.
                   It requires Prometheus >= v2.27.0.

                sendNativeHistograms	<boolean>
                  Enables sending of native histograms, also known as sparse histograms over
                  remote write.
                   It requires Prometheus >= v2.40.0.

                sigv4	<Object>
                  Sigv4 allows to configures AWS's Signature Verification 4 for the URL.
                   It requires Prometheus >= v2.26.0.
                   Cannot be set at the same time as `authorization`, `basicAuth`, `oauth2`,
                  or `azureAd`.

                tlsConfig	<Object>
                  TLS Config to use for the URL.

                url	<string> -required-
                  The URL of the endpoint to send samples to.

                writeRelabelConfigs	<[]Object>
                  The list of remote write relabel configurations.

            replica_external_label_name(str): Name of Prometheus external label used to denote the replica name. The
              external label will _not_ be added when the field is set to the empty string
              (`""`).
               Default: "prometheus_replica"

            replicas(int): Number of replicas of each shard to deploy for a Prometheus deployment.
              `spec.replicas` multiplied by `spec.shards` is the total number of Pods
              created.
               Default: 1

            resources(Dict[Any, Any]): Defines the resources requests and limits of the 'prometheus' container.

              FIELDS:
                claims	<[]Object>
                  Claims lists the names of resources, defined in spec.resourceClaims, that
                  are used by this container.
                   This is an alpha field and requires enabling the DynamicResourceAllocation
                  feature gate.
                   This field is immutable. It can only be set for containers.

                limits	<map[string]Object>
                  Limits describes the maximum amount of compute resources allowed. More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

                requests	<map[string]Object>
                  Requests describes the minimum amount of compute resources required. If
                  Requests is omitted for a container, it defaults to Limits if that is
                  explicitly specified, otherwise to an implementation-defined value. Requests
                  cannot exceed Limits. More info:
                  https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

            retention(str): How long to retain the Prometheus data.
               Default: "24h" if `spec.retention` and `spec.retentionSize` are empty.

            retention_size(str): Maximum number of bytes used by the Prometheus data.

            route_prefix(str): The route prefix Prometheus registers HTTP handlers for.
               This is useful when using `spec.externalURL`, and a proxy is rewriting HTTP
              routes of a request, and the actual ExternalURL is still true, but the
              server serves requests under a different route prefix. For example for use
              with `kubectl proxy`.

            rule_namespace_selector(Dict[Any, Any]): Namespaces to match for PrometheusRule discovery. An empty label selector
              matches all namespaces. A null label selector matches the current namespace
              only.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            rule_selector(Dict[Any, Any]): PrometheusRule objects to be selected for rule evaluation. An empty label
              selector matches all objects. A null label selector matches no objects.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            rules(Dict[Any, Any]): Defines the configuration of the Prometheus rules' engine.

              FIELDS:
                alert	<Object>
                  Defines the parameters of the Prometheus rules' engine.
                   Any update to these parameters trigger a restart of the pods.

            sample_limit(int): SampleLimit defines per-scrape limit on number of scraped samples that will
              be accepted. Only valid in Prometheus versions 2.45.0 and newer.

            scrape_classes(List[Any]): List of scrape classes to expose to scraping objects such as PodMonitors,
              ServiceMonitors, Probes and ScrapeConfigs.
               This is an *experimental feature*, it may change in any upcoming release in
              a breaking way.

              FIELDS:
                default	<boolean>
                  Default indicates that the scrape applies to all scrape objects that don't
                  configure an explicit scrape class name.
                   Only one scrape class can be set as default.

                name	<string> -required-
                  Name of the scrape class.

                relabelings	<[]Object>
                  Relabelings configures the relabeling rules to apply to all scrape targets.
                   The Operator automatically adds relabelings for a few standard Kubernetes
                  fields like `__meta_kubernetes_namespace` and
                  `__meta_kubernetes_service_name`. Then the Operator adds the scrape class
                  relabelings defined here. Then the Operator adds the target-specific
                  relabelings defined in the scrape object.
                   More info:
                  https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config

                tlsConfig	<Object>
                  TLSConfig section for scrapes.

            scrape_config_namespace_selector(Dict[Any, Any]): Namespaces to match for ScrapeConfig discovery. An empty label selector
              matches all namespaces. A null label selector matches the current namespace
              only.
               Note that the ScrapeConfig custom resource definition is currently at Alpha
              level.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            scrape_config_selector(Dict[Any, Any]): ScrapeConfigs to be selected for target discovery. An empty label selector
              matches all objects. A null label selector matches no objects.
               If `spec.serviceMonitorSelector`, `spec.podMonitorSelector`,
              `spec.probeSelector` and `spec.scrapeConfigSelector` are null, the
              Prometheus configuration is unmanaged. The Prometheus operator will ensure
              that the Prometheus configuration's Secret exists, but it is the
              responsibility of the user to provide the raw gzipped Prometheus
              configuration under the `prometheus.yaml.gz` key. This behavior is
              *deprecated* and will be removed in the next major version of the custom
              resource definition. It is recommended to use `spec.additionalScrapeConfigs`
              instead.
               Note that the ScrapeConfig custom resource definition is currently at Alpha
              level.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            scrape_interval(str): Interval between consecutive scrapes.
               Default: "30s"

            scrape_protocols(Dict[Any, Any]): The protocols to negotiate during a scrape. It tells clients the protocols
              supported by Prometheus in order of preference (from most to least
              preferred).
               If unset, Prometheus uses its default value.
               It requires Prometheus >= v2.49.0.
              ScrapeProtocol represents a protocol used by Prometheus for scraping
              metrics. Supported values are: * `OpenMetricsText0.0.1` *
              `OpenMetricsText1.0.0` * `PrometheusProto` * `PrometheusText0.0.4`

            scrape_timeout(str): Number of seconds to wait until a scrape request times out.

            secrets(Dict[Any, Any]): Secrets is a list of Secrets in the same namespace as the Prometheus object,
              which shall be mounted into the Prometheus Pods. Each Secret is added to the
              StatefulSet definition as a volume named `secret-<secret-name>`. The Secrets
              are mounted into /etc/prometheus/secrets/<secret-name> in the 'prometheus'
              container.

            security_context(Dict[Any, Any]): SecurityContext holds pod-level security attributes and common container
              settings. This defaults to the default PodSecurityContext.

              FIELDS:
                fsGroup	<integer>
                  A special supplemental group that applies to all containers in a pod. Some
                  volume types allow the Kubelet to change the ownership of that volume to be
                  owned by the pod:
                   1. The owning GID will be the FSGroup 2. The setgid bit is set (new files
                  created in the volume will be owned by FSGroup) 3. The permission bits are
                  OR'd with rw-rw----
                   If unset, the Kubelet will not modify the ownership and permissions of any
                  volume. Note that this field cannot be set when spec.os.name is windows.

                fsGroupChangePolicy	<string>
                  fsGroupChangePolicy defines behavior of changing ownership and permission of
                  the volume before being exposed inside Pod. This field will only apply to
                  volume types which support fsGroup based ownership(and permissions). It will
                  have no effect on ephemeral volume types such as: secret, configmaps and
                  emptydir. Valid values are "OnRootMismatch" and "Always". If not specified,
                  "Always" is used. Note that this field cannot be set when spec.os.name is
                  windows.

                runAsGroup	<integer>
                  The GID to run the entrypoint of the container process. Uses runtime default
                  if unset. May also be set in SecurityContext.  If set in both
                  SecurityContext and PodSecurityContext, the value specified in
                  SecurityContext takes precedence for that container. Note that this field
                  cannot be set when spec.os.name is windows.

                runAsNonRoot	<boolean>
                  Indicates that the container must run as a non-root user. If true, the
                  Kubelet will validate the image at runtime to ensure that it does not run as
                  UID 0 (root) and fail to start the container if it does. If unset or false,
                  no such validation will be performed. May also be set in SecurityContext.
                  If set in both SecurityContext and PodSecurityContext, the value specified
                  in SecurityContext takes precedence.

                runAsUser	<integer>
                  The UID to run the entrypoint of the container process. Defaults to user
                  specified in image metadata if unspecified. May also be set in
                  SecurityContext.  If set in both SecurityContext and PodSecurityContext, the
                  value specified in SecurityContext takes precedence for that container. Note
                  that this field cannot be set when spec.os.name is windows.

                seLinuxOptions	<Object>
                  The SELinux context to be applied to all containers. If unspecified, the
                  container runtime will allocate a random SELinux context for each container.
                  May also be set in SecurityContext.  If set in both SecurityContext and
                  PodSecurityContext, the value specified in SecurityContext takes precedence
                  for that container. Note that this field cannot be set when spec.os.name is
                  windows.

                seccompProfile	<Object>
                  The seccomp options to use by the containers in this pod. Note that this
                  field cannot be set when spec.os.name is windows.

                supplementalGroups	<[]integer>
                  A list of groups applied to the first process run in each container, in
                  addition to the container's primary GID, the fsGroup (if specified), and
                  group memberships defined in the container image for the uid of the
                  container process. If unspecified, no additional groups are added to any
                  container. Note that group memberships defined in the container image for
                  the uid of the container process are still effective, even if they are not
                  included in this list. Note that this field cannot be set when spec.os.name
                  is windows.

                sysctls	<[]Object>
                  Sysctls hold a list of namespaced sysctls used for the pod. Pods with
                  unsupported sysctls (by the container runtime) might fail to launch. Note
                  that this field cannot be set when spec.os.name is windows.

                windowsOptions	<Object>
                  The Windows specific settings applied to all containers. If unspecified, the
                  options within a container's SecurityContext will be used. If set in both
                  SecurityContext and PodSecurityContext, the value specified in
                  SecurityContext takes precedence. Note that this field cannot be set when
                  spec.os.name is linux.

            service_account_name(str): ServiceAccountName is the name of the ServiceAccount to use to run the
              Prometheus Pods.

            service_monitor_namespace_selector(Dict[Any, Any]): Namespaces to match for ServicedMonitors discovery. An empty label selector
              matches all namespaces. A null label selector matches the current namespace
              only.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            service_monitor_selector(Dict[Any, Any]): ServiceMonitors to be selected for target discovery. An empty label selector
              matches all objects. A null label selector matches no objects.
               If `spec.serviceMonitorSelector`, `spec.podMonitorSelector`,
              `spec.probeSelector` and `spec.scrapeConfigSelector` are null, the
              Prometheus configuration is unmanaged. The Prometheus operator will ensure
              that the Prometheus configuration's Secret exists, but it is the
              responsibility of the user to provide the raw gzipped Prometheus
              configuration under the `prometheus.yaml.gz` key. This behavior is
              *deprecated* and will be removed in the next major version of the custom
              resource definition. It is recommended to use `spec.additionalScrapeConfigs`
              instead.

              FIELDS:
                matchExpressions	<[]Object>
                  matchExpressions is a list of label selector requirements. The requirements
                  are ANDed.

                matchLabels	<map[string]string>
                  matchLabels is a map of {key,value} pairs. A single {key,value} in the
                  matchLabels map is equivalent to an element of matchExpressions, whose key
                  field is "key", the operator is "In", and the values array contains only
                  "value". The requirements are ANDed.

            sha(str): Deprecated: use 'spec.image' instead. The image's digest can be specified as
              part of the image name.

            shards(int): Number of shards to distribute targets onto. `spec.replicas` multiplied by
              `spec.shards` is the total number of Pods created.
               Note that scaling down shards will not reshard data onto remaining
              instances, it must be manually moved. Increasing shards will not reshard
              data either but it will continue to be available from the same instances. To
              query globally, use Thanos sidecar and Thanos querier or remote write data
              to a central location.
               Sharding is performed on the content of the `__address__` target meta-label
              for PodMonitors and ServiceMonitors and `__param_target__` for Probes.
               Default: 1

            storage(Dict[Any, Any]): Storage defines the storage used by Prometheus.

              FIELDS:
                disableMountSubPath	<boolean>
                  Deprecated: subPath usage will be removed in a future release.

                emptyDir	<Object>
                  EmptyDirVolumeSource to be used by the StatefulSet. If specified, it takes
                  precedence over `ephemeral` and `volumeClaimTemplate`. More info:
                  https://kubernetes.io/docs/concepts/storage/volumes/#emptydir

                ephemeral	<Object>
                  EphemeralVolumeSource to be used by the StatefulSet. This is a beta field in
                  k8s 1.21 and GA in 1.15. For lower versions, starting with k8s 1.19, it
                  requires enabling the GenericEphemeralVolume feature gate. More info:
                  https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/#generic-ephemeral-volumes

                volumeClaimTemplate	<Object>
                  Defines the PVC spec to be used by the Prometheus StatefulSets. The easiest
                  way to use a volume that cannot be automatically provisioned is to use a
                  label selector alongside manually created PersistentVolumes.

            tag(str): Deprecated: use 'spec.image' instead. The image's tag can be specified as
              part of the image name.

            target_limit(int): TargetLimit defines a limit on the number of scraped targets that will be
              accepted. Only valid in Prometheus versions 2.45.0 and newer.

            thanos(Dict[Any, Any]): Defines the configuration of the optional Thanos sidecar.

              FIELDS:
                additionalArgs	<[]Object>
                  AdditionalArgs allows setting additional arguments for the Thanos container.
                  The arguments are passed as-is to the Thanos container which may cause
                  issues if they are invalid or not supported the given Thanos version. In
                  case of an argument conflict (e.g. an argument which is already set by the
                  operator itself) or when providing an invalid argument, the reconciliation
                  will fail and an error will be logged.

                baseImage	<string>
                  Deprecated: use 'image' instead.

                blockSize	<string>
                  BlockDuration controls the size of TSDB blocks produced by Prometheus. The
                  default value is 2h to match the upstream Prometheus defaults.
                   WARNING: Changing the block duration can impact the performance and
                  efficiency of the entire Prometheus/Thanos stack due to how it interacts
                  with memory and Thanos compactors. It is recommended to keep this value set
                  to a multiple of 120 times your longest scrape or rule interval. For
                  example, 30s * 120 = 1h.

                getConfigInterval	<string>
                  How often to retrieve the Prometheus configuration.

                getConfigTimeout	<string>
                  Maximum time to wait when retrieving the Prometheus configuration.

                grpcListenLocal	<boolean>
                  When true, the Thanos sidecar listens on the loopback interface instead of
                  the Pod IP's address for the gRPC endpoints.
                   It has no effect if `listenLocal` is true.

                grpcServerTlsConfig	<Object>
                  Configures the TLS parameters for the gRPC server providing the StoreAPI.
                   Note: Currently only the `caFile`, `certFile`, and `keyFile` fields are
                  supported.

                httpListenLocal	<boolean>
                  When true, the Thanos sidecar listens on the loopback interface instead of
                  the Pod IP's address for the HTTP endpoints.
                   It has no effect if `listenLocal` is true.

                image	<string>
                  Container image name for Thanos. If specified, it takes precedence over the
                  `spec.thanos.baseImage`, `spec.thanos.tag` and `spec.thanos.sha` fields.
                   Specifying `spec.thanos.version` is still necessary to ensure the
                  Prometheus Operator knows which version of Thanos is being configured.
                   If neither `spec.thanos.image` nor `spec.thanos.baseImage` are defined, the
                  operator will use the latest upstream version of Thanos available at the
                  time when the operator was released.

                listenLocal	<boolean>
                  Deprecated: use `grpcListenLocal` and `httpListenLocal` instead.

                logFormat	<string>
                  Log format for the Thanos sidecar.

                logLevel	<string>
                  Log level for the Thanos sidecar.

                minTime	<string>
                  Defines the start of time range limit served by the Thanos sidecar's
                  StoreAPI. The field's value should be a constant time in RFC3339 format or a
                  time duration relative to current time, such as -1d or 2h45m. Valid duration
                  units are ms, s, m, h, d, w, y.

                objectStorageConfig	<Object>
                  Defines the Thanos sidecar's configuration to upload TSDB blocks to object
                  storage.
                   More info: https://thanos.io/tip/thanos/storage.md/
                   objectStorageConfigFile takes precedence over this field.

                objectStorageConfigFile	<string>
                  Defines the Thanos sidecar's configuration file to upload TSDB blocks to
                  object storage.
                   More info: https://thanos.io/tip/thanos/storage.md/
                   This field takes precedence over objectStorageConfig.

                readyTimeout	<string>
                  ReadyTimeout is the maximum time that the Thanos sidecar will wait for
                  Prometheus to start.

                resources	<Object>
                  Defines the resources requests and limits of the Thanos sidecar.

                sha	<string>
                  Deprecated: use 'image' instead.  The image digest can be specified as part
                  of the image name.

                tag	<string>
                  Deprecated: use 'image' instead. The image's tag can be specified as as part
                  of the image name.

                tracingConfig	<Object>
                  Defines the tracing configuration for the Thanos sidecar.
                   `tracingConfigFile` takes precedence over this field.
                   More info: https://thanos.io/tip/thanos/tracing.md/
                   This is an *experimental feature*, it may change in any upcoming release in
                  a breaking way.

                tracingConfigFile	<string>
                  Defines the tracing configuration file for the Thanos sidecar.
                   This field takes precedence over `tracingConfig`.
                   More info: https://thanos.io/tip/thanos/tracing.md/
                   This is an *experimental feature*, it may change in any upcoming release in
                  a breaking way.

                version	<string>
                  Version of Thanos being deployed. The operator uses this information to
                  generate the Prometheus StatefulSet + configuration files.
                   If not specified, the operator assumes the latest upstream release of
                  Thanos available at the time when the version of the operator was released.

                volumeMounts	<[]Object>
                  VolumeMounts allows configuration of additional VolumeMounts for Thanos.
                  VolumeMounts specified will be appended to other VolumeMounts in the
                  'thanos-sidecar' container.

            tolerations(List[Any]): Defines the Pods' tolerations if specified.
              The pod this Toleration is attached to tolerates any taint that matches the
              triple <key,value,effect> using the matching operator <operator>.

              FIELDS:
                effect	<string>
                  Effect indicates the taint effect to match. Empty means match all taint
                  effects. When specified, allowed values are NoSchedule, PreferNoSchedule and
                  NoExecute.

                key	<string>
                  Key is the taint key that the toleration applies to. Empty means match all
                  taint keys. If the key is empty, operator must be Exists; this combination
                  means to match all values and all keys.

                operator	<string>
                  Operator represents a key's relationship to the value. Valid operators are
                  Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for
                  value, so that a pod can tolerate all taints of a particular category.

                tolerationSeconds	<integer>
                  TolerationSeconds represents the period of time the toleration (which must
                  be of effect NoExecute, otherwise this field is ignored) tolerates the
                  taint. By default, it is not set, which means tolerate the taint forever (do
                  not evict). Zero and negative values will be treated as 0 (evict
                  immediately) by the system.

                value	<string>
                  Value is the taint value the toleration matches to. If the operator is
                  Exists, the value should be empty, otherwise just a regular string.

            topology_spread_constraints(List[Any]): Defines the pod's topology spread constraints if specified.

              FIELDS:
                additionalLabelSelectors	<string>
                  Defines what Prometheus Operator managed labels should be added to
                  labelSelector on the topologySpreadConstraint.

                labelSelector	<Object>
                  LabelSelector is used to find matching pods. Pods that match this label
                  selector are counted to determine the number of pods in their corresponding
                  topology domain.

                matchLabelKeys	<[]string>
                  MatchLabelKeys is a set of pod label keys to select the pods over which
                  spreading will be calculated. The keys are used to lookup values from the
                  incoming pod labels, those key-value labels are ANDed with labelSelector to
                  select the group of existing pods over which spreading will be calculated
                  for the incoming pod. The same key is forbidden to exist in both
                  MatchLabelKeys and LabelSelector. MatchLabelKeys cannot be set when
                  LabelSelector isn't set. Keys that don't exist in the incoming pod labels
                  will be ignored. A null or empty list means only match against
                  labelSelector.
                   This is a beta field and requires the MatchLabelKeysInPodTopologySpread
                  feature gate to be enabled (enabled by default).

                maxSkew	<integer> -required-
                  MaxSkew describes the degree to which pods may be unevenly distributed. When
                  `whenUnsatisfiable=DoNotSchedule`, it is the maximum permitted difference
                  between the number of matching pods in the target topology and the global
                  minimum. The global minimum is the minimum number of matching pods in an
                  eligible domain or zero if the number of eligible domains is less than
                  MinDomains. For example, in a 3-zone cluster, MaxSkew is set to 1, and pods
                  with the same labelSelector spread as 2/2/1: In this case, the global
                  minimum is 1. | zone1 | zone2 | zone3 | |  P P  |  P P  |   P   | - if
                  MaxSkew is 1, incoming pod can only be scheduled to zone3 to become 2/2/2;
                  scheduling it onto zone1(zone2) would make the ActualSkew(3-1) on
                  zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be
                  scheduled onto any zone. When `whenUnsatisfiable=ScheduleAnyway`, it is used
                  to give higher precedence to topologies that satisfy it. It's a required
                  field. Default value is 1 and 0 is not allowed.

                minDomains	<integer>
                  MinDomains indicates a minimum number of eligible domains. When the number
                  of eligible domains with matching topology keys is less than minDomains, Pod
                  Topology Spread treats "global minimum" as 0, and then the calculation of
                  Skew is performed. And when the number of eligible domains with matching
                  topology keys equals or greater than minDomains, this value has no effect on
                  scheduling. As a result, when the number of eligible domains is less than
                  minDomains, scheduler won't schedule more than maxSkew Pods to those
                  domains. If value is nil, the constraint behaves as if MinDomains is equal
                  to 1. Valid values are integers greater than 0. When value is not nil,
                  WhenUnsatisfiable must be DoNotSchedule.
                   For example, in a 3-zone cluster, MaxSkew is set to 2, MinDomains is set to
                  5 and pods with the same labelSelector spread as 2/2/2: | zone1 | zone2 |
                  zone3 | |  P P  |  P P  |  P P  | The number of domains is less than
                  5(MinDomains), so "global minimum" is treated as 0. In this situation, new
                  pod with the same labelSelector cannot be scheduled, because computed skew
                  will be 3(3 - 0) if new Pod is scheduled to any of the three zones, it will
                  violate MaxSkew.
                   This is a beta field and requires the MinDomainsInPodTopologySpread feature
                  gate to be enabled (enabled by default).

                nodeAffinityPolicy	<string>
                  NodeAffinityPolicy indicates how we will treat Pod's
                  nodeAffinity/nodeSelector when calculating pod topology spread skew. Options
                  are: - Honor: only nodes matching nodeAffinity/nodeSelector are included in
                  the calculations. - Ignore: nodeAffinity/nodeSelector are ignored. All nodes
                  are included in the calculations.
                   If this value is nil, the behavior is equivalent to the Honor policy. This
                  is a beta-level feature default enabled by the
                  NodeInclusionPolicyInPodTopologySpread feature flag.

                nodeTaintsPolicy	<string>
                  NodeTaintsPolicy indicates how we will treat node taints when calculating
                  pod topology spread skew. Options are: - Honor: nodes without taints, along
                  with tainted nodes for which the incoming pod has a toleration, are
                  included. - Ignore: node taints are ignored. All nodes are included.
                   If this value is nil, the behavior is equivalent to the Ignore policy. This
                  is a beta-level feature default enabled by the
                  NodeInclusionPolicyInPodTopologySpread feature flag.

                topologyKey	<string> -required-
                  TopologyKey is the key of node labels. Nodes that have a label with this key
                  and identical values are considered to be in the same topology. We consider
                  each <key, value> as a "bucket", and try to put balanced number of pods into
                  each bucket. We define a domain as a particular instance of a topology.
                  Also, we define an eligible domain as a domain whose nodes meet the
                  requirements of nodeAffinityPolicy and nodeTaintsPolicy. e.g. If TopologyKey
                  is "kubernetes.io/hostname", each Node is a domain of that topology. And, if
                  TopologyKey is "topology.kubernetes.io/zone", each zone is a domain of that
                  topology. It's a required field.

                whenUnsatisfiable	<string> -required-
                  WhenUnsatisfiable indicates how to deal with a pod if it doesn't satisfy the
                  spread constraint. - DoNotSchedule (default) tells the scheduler not to
                  schedule it. - ScheduleAnyway tells the scheduler to schedule the pod in any
                  location, but giving higher precedence to topologies that would help reduce
                  the skew. A constraint is considered "Unsatisfiable" for an incoming pod if
                  and only if every possible node assignment for that pod would violate
                  "MaxSkew" on some topology. For example, in a 3-zone cluster, MaxSkew is set
                  to 1, and pods with the same labelSelector spread as 3/1/1: | zone1 | zone2
                  | zone3 | | P P P |   P   |   P   | If WhenUnsatisfiable is set to
                  DoNotSchedule, incoming pod can only be scheduled to zone2(zone3) to become
                  3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In
                  other words, the cluster can still be imbalanced, but scheduler won't make
                  it *more* imbalanced. It's a required field.

            tracing_config(Dict[Any, Any]): TracingConfig configures tracing in Prometheus.
               This is an *experimental feature*, it may change in any upcoming release in
              a breaking way.

              FIELDS:
                clientType	<string>
                  Client used to export the traces. Supported values are `http` or `grpc`.

                compression	<string>
                  Compression key for supported compression types. The only supported value is
                  `gzip`.

                endpoint	<string> -required-
                  Endpoint to send the traces to. Should be provided in format <host>:<port>.

                headers	<map[string]string>
                  Key-value pairs to be used as headers associated with gRPC or HTTP requests.

                insecure	<boolean>
                  If disabled, the client will use a secure connection.

                samplingFraction	<Object>
                  Sets the probability a given trace will be sampled. Must be a float from 0
                  through 1.

                timeout	<string>
                  Maximum time the exporter will wait for each batch export.

                tlsConfig	<Object>
                  TLS Config to use when sending traces.

            tsdb(Dict[Any, Any]): Defines the runtime reloadable configuration of the timeseries database
              (TSDB).

              FIELDS:
                outOfOrderTimeWindow	<string>
                  Configures how old an out-of-order/out-of-bounds sample can be with respect
                  to the TSDB max time.
                   An out-of-order/out-of-bounds sample is ingested into the TSDB as long as
                  the timestamp of the sample is >= (TSDB.MaxTime - outOfOrderTimeWindow).
                   This is an *experimental feature*, it may change in any upcoming release in
                  a breaking way.
                   It requires Prometheus >= v2.39.0.

            version(str): Version of Prometheus being deployed. The operator uses this information to
              generate the Prometheus StatefulSet + configuration files.
               If not specified, the operator assumes the latest upstream version of
              Prometheus available at the time when the version of the operator was
              released.

            volume_mounts(List[Any]): VolumeMounts allows the configuration of additional VolumeMounts.
               VolumeMounts will be appended to other VolumeMounts in the 'prometheus'
              container, that are generated as a result of StorageSpec objects.
              VolumeMount describes a mounting of a Volume within a container.

              FIELDS:
                mountPath	<string> -required-
                  Path within the container at which the volume should be mounted.  Must not
                  contain ':'.

                mountPropagation	<string>
                  mountPropagation determines how mounts are propagated from the host to
                  container and the other way around. When not set, MountPropagationNone is
                  used. This field is beta in 1.10.

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
                  mounted. Behaves similarly to SubPath but environment variable references
                  $(VAR_NAME) are expanded using the container's environment. Defaults to ""
                  (volume's root). SubPathExpr and SubPath are mutually exclusive.

            volumes(List[Any]): Volumes allows the configuration of additional volumes on the output
              StatefulSet definition. Volumes specified will be appended to other volumes
              that are generated as a result of StorageSpec objects.
              Volume represents a named volume in a pod that may be accessed by any
              container in the pod.

              FIELDS:
                awsElasticBlockStore	<Object>
                  awsElasticBlockStore represents an AWS Disk resource that is attached to a
                  kubelet's host machine and then exposed to the pod. More info:
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
                  machine. More info: https://examples.k8s.io/mysql-cinder-pd/README.md

                configMap	<Object>
                  configMap represents a configMap that should populate this volume

                csi	<Object>
                  csi (Container Storage Interface) represents ephemeral storage that is
                  handled by certain external CSI drivers (Beta feature).

                downwardAPI	<Object>
                  downwardAPI represents downward API about the pod that should populate this
                  volume

                emptyDir	<Object>
                  emptyDir represents a temporary directory that shares a pod's lifetime. More
                  info: https://kubernetes.io/docs/concepts/storage/volumes#emptydir

                ephemeral	<Object>
                  ephemeral represents a volume that is handled by a cluster storage driver.
                  The volume's lifecycle is tied to the pod that defines it - it will be
                  created before the pod starts, and deleted when the pod is removed.
                   Use this if: a) the volume is only needed while the pod runs, b) features
                  of normal volumes like restoring from snapshot or capacity tracking are
                  needed, c) the storage driver is specified through a storage class, and d)
                  the storage driver supports dynamic volume provisioning through a
                  PersistentVolumeClaim (see EphemeralVolumeSource for more information on the
                  connection between this volume type and PersistentVolumeClaim).
                   Use PersistentVolumeClaim or one of the vendor-specific APIs for volumes
                  that persist for longer than the lifecycle of an individual pod.
                   Use CSI for light-weight local ephemeral volumes if the CSI driver is meant
                  to be used that way - see the documentation of the driver for more
                  information.
                   A pod can use both types of ephemeral volumes and persistent volumes at the
                  same time.

                fc	<Object>
                  fc represents a Fibre Channel resource that is attached to a kubelet's host
                  machine and then exposed to the pod.

                flexVolume	<Object>
                  flexVolume represents a generic volume resource that is provisioned/attached
                  using an exec based plugin.

                flocker	<Object>
                  flocker represents a Flocker volume attached to a kubelet's host machine.
                  This depends on the Flocker control service being running

                gcePersistentDisk	<Object>
                  gcePersistentDisk represents a GCE Disk resource that is attached to a
                  kubelet's host machine and then exposed to the pod. More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk

                gitRepo	<Object>
                  gitRepo represents a git repository at a particular revision. DEPRECATED:
                  GitRepo is deprecated. To provision a container with a git repo, mount an
                  EmptyDir into an InitContainer that clones the repo using git, then mount
                  the EmptyDir into the Pod's container.

                glusterfs	<Object>
                  glusterfs represents a Glusterfs mount on the host that shares a pod's
                  lifetime. More info: https://examples.k8s.io/volumes/glusterfs/README.md

                hostPath	<Object>
                  hostPath represents a pre-existing file or directory on the host machine
                  that is directly exposed to the container. This is generally used for system
                  agents or other privileged things that are allowed to see the host machine.
                  Most containers will NOT need this. More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#hostpath ---
                  TODO(jonesdl) We need to restrict who can use host directory mounts and who
                  can/can not mount host directories as read/write.

                iscsi	<Object>
                  iscsi represents an ISCSI Disk resource that is attached to a kubelet's host
                  machine and then exposed to the pod. More info:
                  https://examples.k8s.io/volumes/iscsi/README.md

                name	<string> -required-
                  name of the volume. Must be a DNS_LABEL and unique within the pod. More
                  info:
                  https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

                nfs	<Object>
                  nfs represents an NFS mount on the host that shares a pod's lifetime More
                  info: https://kubernetes.io/docs/concepts/storage/volumes#nfs

                persistentVolumeClaim	<Object>
                  persistentVolumeClaimVolumeSource represents a reference to a
                  PersistentVolumeClaim in the same namespace. More info:
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
                  lifetime. More info: https://examples.k8s.io/volumes/rbd/README.md

                scaleIO	<Object>
                  scaleIO represents a ScaleIO persistent volume attached and mounted on
                  Kubernetes nodes.

                secret	<Object>
                  secret represents a secret that should populate this volume. More info:
                  https://kubernetes.io/docs/concepts/storage/volumes#secret

                storageos	<Object>
                  storageOS represents a StorageOS volume attached and mounted on Kubernetes
                  nodes.

                vsphereVolume	<Object>
                  vsphereVolume represents a vSphere volume attached and mounted on kubelets
                  host machine

            wal_compression(bool): Configures compression of the write-ahead log (WAL) using Snappy.
               WAL compression is enabled by default for Prometheus >= 2.20.0
               Requires Prometheus v2.11.0 and above.

            web(Dict[Any, Any]): Defines the configuration of the Prometheus web server.

              FIELDS:
                httpConfig	<Object>
                  Defines HTTP parameters for web server.

                maxConnections	<integer>
                  Defines the maximum number of simultaneous connections A zero value means
                  that Prometheus doesn't accept any incoming connection.

                pageTitle	<string>
                  The prometheus web page title.

                tlsConfig	<Object>
                  Defines the TLS parameters for HTTPS.

        """
        super().__init__(**kwargs)

        self.additional_alert_manager_configs = additional_alert_manager_configs
        self.additional_alert_relabel_configs = additional_alert_relabel_configs
        self.additional_args = additional_args
        self.additional_scrape_configs = additional_scrape_configs
        self.affinity = affinity
        self.alerting = alerting
        self.allow_overlapping_blocks = allow_overlapping_blocks
        self.apiserver_config = apiserver_config
        self.arbitrary_fs_access_through_sms = arbitrary_fs_access_through_sms
        self.base_image = base_image
        self.body_size_limit = body_size_limit
        self.config_maps = config_maps
        self.containers = containers
        self.disable_compaction = disable_compaction
        self.enable_admin_api = enable_admin_api
        self.enable_features = enable_features
        self.enable_remote_write_receiver = enable_remote_write_receiver
        self.enforced_body_size_limit = enforced_body_size_limit
        self.enforced_keep_dropped_targets = enforced_keep_dropped_targets
        self.enforced_label_limit = enforced_label_limit
        self.enforced_label_name_length_limit = enforced_label_name_length_limit
        self.enforced_label_value_length_limit = enforced_label_value_length_limit
        self.enforced_namespace_label = enforced_namespace_label
        self.enforced_sample_limit = enforced_sample_limit
        self.enforced_target_limit = enforced_target_limit
        self.evaluation_interval = evaluation_interval
        self.excluded_from_enforcement = excluded_from_enforcement
        self.exemplars = exemplars
        self.external_labels = external_labels
        self.external_url = external_url
        self.host_aliases = host_aliases
        self.host_network = host_network
        self.ignore_namespace_selectors = ignore_namespace_selectors
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.init_containers = init_containers
        self.keep_dropped_targets = keep_dropped_targets
        self.label_limit = label_limit
        self.label_name_length_limit = label_name_length_limit
        self.label_value_length_limit = label_value_length_limit
        self.listen_local = listen_local
        self.log_format = log_format
        self.log_level = log_level
        self.maximum_startup_duration_seconds = maximum_startup_duration_seconds
        self.min_ready_seconds = min_ready_seconds
        self.node_selector = node_selector
        self.override_honor_labels = override_honor_labels
        self.override_honor_timestamps = override_honor_timestamps
        self.paused = paused
        self.persistent_volume_claim_retention_policy = persistent_volume_claim_retention_policy
        self.pod_metadata = pod_metadata
        self.pod_monitor_namespace_selector = pod_monitor_namespace_selector
        self.pod_monitor_selector = pod_monitor_selector
        self.pod_target_labels = pod_target_labels
        self.port_name = port_name
        self.priority_class_name = priority_class_name
        self.probe_namespace_selector = probe_namespace_selector
        self.probe_selector = probe_selector
        self.prometheus_external_label_name = prometheus_external_label_name
        self.prometheus_rules_excluded_from_enforce = prometheus_rules_excluded_from_enforce
        self.query = query
        self.query_log_file = query_log_file
        self.reload_strategy = reload_strategy
        self.remote_read = remote_read
        self.remote_write = remote_write
        self.replica_external_label_name = replica_external_label_name
        self.replicas = replicas
        self.resources = resources
        self.retention = retention
        self.retention_size = retention_size
        self.route_prefix = route_prefix
        self.rule_namespace_selector = rule_namespace_selector
        self.rule_selector = rule_selector
        self.rules = rules
        self.sample_limit = sample_limit
        self.scrape_classes = scrape_classes
        self.scrape_config_namespace_selector = scrape_config_namespace_selector
        self.scrape_config_selector = scrape_config_selector
        self.scrape_interval = scrape_interval
        self.scrape_protocols = scrape_protocols
        self.scrape_timeout = scrape_timeout
        self.secrets = secrets
        self.security_context = security_context
        self.service_account_name = service_account_name
        self.service_monitor_namespace_selector = service_monitor_namespace_selector
        self.service_monitor_selector = service_monitor_selector
        self.sha = sha
        self.shards = shards
        self.storage = storage
        self.tag = tag
        self.target_limit = target_limit
        self.thanos = thanos
        self.tolerations = tolerations
        self.topology_spread_constraints = topology_spread_constraints
        self.tracing_config = tracing_config
        self.tsdb = tsdb
        self.version = version
        self.volume_mounts = volume_mounts
        self.volumes = volumes
        self.wal_compression = wal_compression
        self.web = web

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.additional_alert_manager_configs:
                _spec["additionalAlertManagerConfigs"] = self.additional_alert_manager_configs

            if self.additional_alert_relabel_configs:
                _spec["additionalAlertRelabelConfigs"] = self.additional_alert_relabel_configs

            if self.additional_args:
                _spec["additionalArgs"] = self.additional_args

            if self.additional_scrape_configs:
                _spec["additionalScrapeConfigs"] = self.additional_scrape_configs

            if self.affinity:
                _spec["affinity"] = self.affinity

            if self.alerting:
                _spec["alerting"] = self.alerting

            if self.allow_overlapping_blocks is not None:
                _spec["allowOverlappingBlocks"] = self.allow_overlapping_blocks

            if self.apiserver_config:
                _spec["apiserverConfig"] = self.apiserver_config

            if self.arbitrary_fs_access_through_sms:
                _spec["arbitraryFSAccessThroughSMs"] = self.arbitrary_fs_access_through_sms

            if self.base_image:
                _spec["baseImage"] = self.base_image

            if self.body_size_limit:
                _spec["bodySizeLimit"] = self.body_size_limit

            if self.config_maps:
                _spec["configMaps"] = self.config_maps

            if self.containers:
                _spec["containers"] = self.containers

            if self.disable_compaction is not None:
                _spec["disableCompaction"] = self.disable_compaction

            if self.enable_admin_api is not None:
                _spec["enableAdminAPI"] = self.enable_admin_api

            if self.enable_features:
                _spec["enableFeatures"] = self.enable_features

            if self.enable_remote_write_receiver is not None:
                _spec["enableRemoteWriteReceiver"] = self.enable_remote_write_receiver

            if self.enforced_body_size_limit:
                _spec["enforcedBodySizeLimit"] = self.enforced_body_size_limit

            if self.enforced_keep_dropped_targets:
                _spec["enforcedKeepDroppedTargets"] = self.enforced_keep_dropped_targets

            if self.enforced_label_limit:
                _spec["enforcedLabelLimit"] = self.enforced_label_limit

            if self.enforced_label_name_length_limit:
                _spec["enforcedLabelNameLengthLimit"] = self.enforced_label_name_length_limit

            if self.enforced_label_value_length_limit:
                _spec["enforcedLabelValueLengthLimit"] = self.enforced_label_value_length_limit

            if self.enforced_namespace_label:
                _spec["enforcedNamespaceLabel"] = self.enforced_namespace_label

            if self.enforced_sample_limit:
                _spec["enforcedSampleLimit"] = self.enforced_sample_limit

            if self.enforced_target_limit:
                _spec["enforcedTargetLimit"] = self.enforced_target_limit

            if self.evaluation_interval:
                _spec["evaluationInterval"] = self.evaluation_interval

            if self.excluded_from_enforcement:
                _spec["excludedFromEnforcement"] = self.excluded_from_enforcement

            if self.exemplars:
                _spec["exemplars"] = self.exemplars

            if self.external_labels:
                _spec["externalLabels"] = self.external_labels

            if self.external_url:
                _spec["externalUrl"] = self.external_url

            if self.host_aliases:
                _spec["hostAliases"] = self.host_aliases

            if self.host_network is not None:
                _spec["hostNetwork"] = self.host_network

            if self.ignore_namespace_selectors is not None:
                _spec["ignoreNamespaceSelectors"] = self.ignore_namespace_selectors

            if self.image:
                _spec["image"] = self.image

            if self.image_pull_policy:
                _spec["imagePullPolicy"] = self.image_pull_policy

            if self.image_pull_secrets:
                _spec["imagePullSecrets"] = self.image_pull_secrets

            if self.init_containers:
                _spec["initContainers"] = self.init_containers

            if self.keep_dropped_targets:
                _spec["keepDroppedTargets"] = self.keep_dropped_targets

            if self.label_limit:
                _spec["labelLimit"] = self.label_limit

            if self.label_name_length_limit:
                _spec["labelNameLengthLimit"] = self.label_name_length_limit

            if self.label_value_length_limit:
                _spec["labelValueLengthLimit"] = self.label_value_length_limit

            if self.listen_local is not None:
                _spec["listenLocal"] = self.listen_local

            if self.log_format:
                _spec["logFormat"] = self.log_format

            if self.log_level:
                _spec["logLevel"] = self.log_level

            if self.maximum_startup_duration_seconds:
                _spec["maximumStartupDurationSeconds"] = self.maximum_startup_duration_seconds

            if self.min_ready_seconds:
                _spec["minReadySeconds"] = self.min_ready_seconds

            if self.node_selector:
                _spec["nodeSelector"] = self.node_selector

            if self.override_honor_labels is not None:
                _spec["overrideHonorLabels"] = self.override_honor_labels

            if self.override_honor_timestamps is not None:
                _spec["overrideHonorTimestamps"] = self.override_honor_timestamps

            if self.paused is not None:
                _spec["paused"] = self.paused

            if self.persistent_volume_claim_retention_policy:
                _spec["persistentVolumeClaimRetentionPolicy"] = self.persistent_volume_claim_retention_policy

            if self.pod_metadata:
                _spec["podMetadata"] = self.pod_metadata

            if self.pod_monitor_namespace_selector:
                _spec["podMonitorNamespaceSelector"] = self.pod_monitor_namespace_selector

            if self.pod_monitor_selector:
                _spec["podMonitorSelector"] = self.pod_monitor_selector

            if self.pod_target_labels:
                _spec["podTargetLabels"] = self.pod_target_labels

            if self.port_name:
                _spec["portName"] = self.port_name

            if self.priority_class_name:
                _spec["priorityClassName"] = self.priority_class_name

            if self.probe_namespace_selector:
                _spec["probeNamespaceSelector"] = self.probe_namespace_selector

            if self.probe_selector:
                _spec["probeSelector"] = self.probe_selector

            if self.prometheus_external_label_name:
                _spec["prometheusExternalLabelName"] = self.prometheus_external_label_name

            if self.prometheus_rules_excluded_from_enforce:
                _spec["prometheusRulesExcludedFromEnforce"] = self.prometheus_rules_excluded_from_enforce

            if self.query:
                _spec["query"] = self.query

            if self.query_log_file:
                _spec["queryLogFile"] = self.query_log_file

            if self.reload_strategy:
                _spec["reloadStrategy"] = self.reload_strategy

            if self.remote_read:
                _spec["remoteRead"] = self.remote_read

            if self.remote_write:
                _spec["remoteWrite"] = self.remote_write

            if self.replica_external_label_name:
                _spec["replicaExternalLabelName"] = self.replica_external_label_name

            if self.replicas:
                _spec["replicas"] = self.replicas

            if self.resources:
                _spec["resources"] = self.resources

            if self.retention:
                _spec["retention"] = self.retention

            if self.retention_size:
                _spec["retentionSize"] = self.retention_size

            if self.route_prefix:
                _spec["routePrefix"] = self.route_prefix

            if self.rule_namespace_selector:
                _spec["ruleNamespaceSelector"] = self.rule_namespace_selector

            if self.rule_selector:
                _spec["ruleSelector"] = self.rule_selector

            if self.rules:
                _spec["rules"] = self.rules

            if self.sample_limit:
                _spec["sampleLimit"] = self.sample_limit

            if self.scrape_classes:
                _spec["scrapeClasses"] = self.scrape_classes

            if self.scrape_config_namespace_selector:
                _spec["scrapeConfigNamespaceSelector"] = self.scrape_config_namespace_selector

            if self.scrape_config_selector:
                _spec["scrapeConfigSelector"] = self.scrape_config_selector

            if self.scrape_interval:
                _spec["scrapeInterval"] = self.scrape_interval

            if self.scrape_protocols:
                _spec["scrapeProtocols"] = self.scrape_protocols

            if self.scrape_timeout:
                _spec["scrapeTimeout"] = self.scrape_timeout

            if self.secrets:
                _spec["secrets"] = self.secrets

            if self.security_context:
                _spec["securityContext"] = self.security_context

            if self.service_account_name:
                _spec["serviceAccountName"] = self.service_account_name

            if self.service_monitor_namespace_selector:
                _spec["serviceMonitorNamespaceSelector"] = self.service_monitor_namespace_selector

            if self.service_monitor_selector:
                _spec["serviceMonitorSelector"] = self.service_monitor_selector

            if self.sha:
                _spec["sha"] = self.sha

            if self.shards:
                _spec["shards"] = self.shards

            if self.storage:
                _spec["storage"] = self.storage

            if self.tag:
                _spec["tag"] = self.tag

            if self.target_limit:
                _spec["targetLimit"] = self.target_limit

            if self.thanos:
                _spec["thanos"] = self.thanos

            if self.tolerations:
                _spec["tolerations"] = self.tolerations

            if self.topology_spread_constraints:
                _spec["topologySpreadConstraints"] = self.topology_spread_constraints

            if self.tracing_config:
                _spec["tracingConfig"] = self.tracing_config

            if self.tsdb:
                _spec["tsdb"] = self.tsdb

            if self.version:
                _spec["version"] = self.version

            if self.volume_mounts:
                _spec["volumeMounts"] = self.volume_mounts

            if self.volumes:
                _spec["volumes"] = self.volumes

            if self.wal_compression is not None:
                _spec["walCompression"] = self.wal_compression

            if self.web:
                _spec["web"] = self.web
