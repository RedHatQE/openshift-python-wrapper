# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/class_generator/README.md


from typing import Any

from ocp_resources.resource import NamespacedResource


class AWX(NamespacedResource):
    """
    Schema validation for the AWX CRD
    """

    api_group: str = NamespacedResource.ApiGroup.AWX_ANSIBLE_COM

    def __init__(
        self,
        additional_labels: list[Any] | None = None,
        admin_email: str | None = None,
        admin_password_secret: str | None = None,
        admin_user: str | None = None,
        affinity: dict[str, Any] | None = None,
        spec_annotations: str | None = None,
        api_urlpattern_prefix: str | None = None,
        spec_api_version: str | None = None,
        auto_upgrade: bool | None = None,
        broadcast_websocket_secret: str | None = None,
        bundle_cacert_secret: str | None = None,
        ca_trust_bundle: str | None = None,
        control_plane_ee_image: str | None = None,
        control_plane_priority_class: str | None = None,
        create_preload_data: bool | None = None,
        csrf_cookie_secure: str | None = None,
        deployment_type: str | None = None,
        development_mode: bool | None = None,
        ee_extra_env: str | None = None,
        ee_extra_volume_mounts: str | None = None,
        ee_images: list[Any] | None = None,
        ee_pull_credentials_secret: str | None = None,
        ee_resource_requirements: dict[str, Any] | None = None,
        extra_settings: list[Any] | None = None,
        extra_settings_files: dict[str, Any] | None = None,
        extra_volumes: str | None = None,
        garbage_collect_secrets: bool | None = None,
        host_aliases: list[Any] | None = None,
        hostname: str | None = None,
        image: str | None = None,
        image_pull_policy: str | None = None,
        image_pull_secret: str | None = None,
        image_pull_secrets: list[Any] | None = None,
        image_version: str | None = None,
        ingress_annotations: str | None = None,
        ingress_api_version: str | None = None,
        ingress_class_name: str | None = None,
        ingress_controller: str | None = None,
        ingress_hosts: list[Any] | None = None,
        ingress_path: str | None = None,
        ingress_path_type: str | None = None,
        ingress_tls_secret: str | None = None,
        ingress_type: str | None = None,
        init_container_extra_commands: str | None = None,
        init_container_extra_volume_mounts: str | None = None,
        init_container_image: str | None = None,
        init_container_image_version: str | None = None,
        init_container_resource_requirements: dict[str, Any] | None = None,
        init_projects_container_image: str | None = None,
        ipv6_disabled: bool | None = None,
        ldap_cacert_secret: str | None = None,
        ldap_password_secret: str | None = None,
        loadbalancer_class: str | None = None,
        loadbalancer_ip: str | None = None,
        loadbalancer_port: int | None = None,
        loadbalancer_protocol: str | None = None,
        metrics_utility_configmap: str | None = None,
        metrics_utility_console_enabled: bool | None = None,
        metrics_utility_cronjob_gather_schedule: str | None = None,
        metrics_utility_cronjob_report_schedule: str | None = None,
        metrics_utility_enabled: bool | None = None,
        metrics_utility_image: str | None = None,
        metrics_utility_image_pull_policy: str | None = None,
        metrics_utility_image_version: str | None = None,
        metrics_utility_pvc_claim: str | None = None,
        metrics_utility_pvc_claim_size: str | None = None,
        metrics_utility_pvc_claim_storage_class: str | None = None,
        metrics_utility_secret: str | None = None,
        metrics_utility_ship_target: str | None = None,
        nginx_listen_queue_size: int | None = None,
        nginx_worker_connections: int | None = None,
        nginx_worker_cpu_affinity: str | None = None,
        nginx_worker_processes: int | None = None,
        no_log: bool | None = None,
        spec_node_selector: str | None = None,
        nodeport_port: int | None = None,
        old_postgres_configuration_secret: str | None = None,
        postgres_configuration_secret: str | None = None,
        postgres_data_volume_init: bool | None = None,
        postgres_extra_args: list[Any] | None = None,
        postgres_extra_volume_mounts: str | None = None,
        postgres_extra_volumes: str | None = None,
        postgres_image: str | None = None,
        postgres_image_version: str | None = None,
        postgres_init_container_commands: str | None = None,
        postgres_init_container_resource_requirements: dict[str, Any] | None = None,
        postgres_keep_pvc_after_upgrade: bool | None = None,
        postgres_keepalives: bool | None = None,
        postgres_keepalives_count: int | None = None,
        postgres_keepalives_idle: int | None = None,
        postgres_keepalives_interval: int | None = None,
        postgres_label_selector: str | None = None,
        postgres_priority_class: str | None = None,
        postgres_resource_requirements: dict[str, Any] | None = None,
        postgres_security_context_settings: dict[str, Any] | None = None,
        postgres_selector: str | None = None,
        postgres_storage_class: str | None = None,
        postgres_storage_requirements: dict[str, Any] | None = None,
        postgres_tolerations: str | None = None,
        projects_existing_claim: str | None = None,
        projects_persistence: bool | None = None,
        projects_storage_access_mode: str | None = None,
        projects_storage_class: str | None = None,
        projects_storage_size: str | None = None,
        projects_use_existing_claim: str | None = None,
        receptor_log_level: str | None = None,
        redis_capabilities: list[Any] | None = None,
        redis_image: str | None = None,
        redis_image_version: str | None = None,
        redis_resource_requirements: dict[str, Any] | None = None,
        replicas: int | None = None,
        route_api_version: str | None = None,
        route_host: str | None = None,
        route_tls_secret: str | None = None,
        route_tls_termination_mechanism: str | None = None,
        rsyslog_args: list[Any] | None = None,
        rsyslog_command: list[Any] | None = None,
        rsyslog_extra_env: str | None = None,
        rsyslog_extra_volume_mounts: str | None = None,
        rsyslog_resource_requirements: dict[str, Any] | None = None,
        secret_key_secret: str | None = None,
        security_context_settings: dict[str, Any] | None = None,
        service_account_annotations: str | None = None,
        service_annotations: str | None = None,
        service_labels: str | None = None,
        service_type: str | None = None,
        session_cookie_secure: str | None = None,
        set_self_labels: bool | None = None,
        task_affinity: dict[str, Any] | None = None,
        task_annotations: str | None = None,
        task_args: list[Any] | None = None,
        task_command: list[Any] | None = None,
        task_extra_env: str | None = None,
        task_extra_volume_mounts: str | None = None,
        task_liveness_failure_threshold: int | None = None,
        task_liveness_initial_delay: int | None = None,
        task_liveness_period: int | None = None,
        task_liveness_timeout: int | None = None,
        task_manage_replicas: bool | None = None,
        task_node_selector: str | None = None,
        task_privileged: bool | None = None,
        task_readiness_failure_threshold: int | None = None,
        task_readiness_initial_delay: int | None = None,
        task_readiness_period: int | None = None,
        task_readiness_timeout: int | None = None,
        task_replicas: int | None = None,
        task_resource_requirements: dict[str, Any] | None = None,
        task_tolerations: str | None = None,
        task_topology_spread_constraints: str | None = None,
        termination_grace_period_seconds: int | None = None,
        tolerations: str | None = None,
        topology_spread_constraints: str | None = None,
        uwsgi_listen_queue_size: int | None = None,
        uwsgi_processes: int | None = None,
        web_affinity: dict[str, Any] | None = None,
        web_annotations: str | None = None,
        web_args: list[Any] | None = None,
        web_command: list[Any] | None = None,
        web_extra_env: str | None = None,
        web_extra_volume_mounts: str | None = None,
        web_liveness_failure_threshold: int | None = None,
        web_liveness_initial_delay: int | None = None,
        web_liveness_period: int | None = None,
        web_liveness_timeout: int | None = None,
        web_manage_replicas: bool | None = None,
        web_node_selector: str | None = None,
        web_readiness_failure_threshold: int | None = None,
        web_readiness_initial_delay: int | None = None,
        web_readiness_period: int | None = None,
        web_readiness_timeout: int | None = None,
        web_replicas: int | None = None,
        web_resource_requirements: dict[str, Any] | None = None,
        web_tolerations: str | None = None,
        web_topology_spread_constraints: str | None = None,
        **kwargs: Any,
    ) -> None:
        r"""
        Args:
            additional_labels (list[Any]): Additional labels defined on the resource, which should be propagated
              to child resources

            admin_email (str): The admin user email

            admin_password_secret (str): Secret where the admin password can be found

            admin_user (str): Username to use for the admin account

            affinity (dict[str, Any]): If specified, the pod's scheduling constraints

            spec_annotations (str): Common annotations for both Web and Task deployments.

            api_urlpattern_prefix (str): An optional configuration to add a prefix in the API URL path

            spec_api_version (str): apiVersion of the deployment type

            auto_upgrade (bool): Should AWX instances be automatically upgraded when operator gets
              upgraded

            broadcast_websocket_secret (str): Secret where the broadcast websocket secret can be found

            bundle_cacert_secret (str): Secret where can be found the trusted Certificate Authority Bundle

            ca_trust_bundle (str): Path where the trusted CA bundle is available

            control_plane_ee_image (str): Registry path to the Execution Environment container image to use on
              control plane pods

            control_plane_priority_class (str): Assign a preexisting priority class to the control plane pods

            create_preload_data (bool): Whether or not to preload data upon instance creation

            csrf_cookie_secure (str): Set csrf cookie secure mode for web

            deployment_type (str): Name of the deployment type

            development_mode (bool): If the deployment should be done in development mode

            ee_extra_env (str): No field description from API

            ee_extra_volume_mounts (str): Specify volume mounts to be added to Execution container

            ee_images (list[Any]): Registry path to the Execution Environment container to use

            ee_pull_credentials_secret (str): Secret where pull credentials for registered ees can be found

            ee_resource_requirements (dict[str, Any]): Resource requirements for the ee container

            extra_settings (list[Any]): Extra settings to specify for AWX

            extra_settings_files (dict[str, Any]): Extra ConfigMaps or Secrets of settings files to specify for AWX

            extra_volumes (str): Specify extra volumes to add to the application pod

            garbage_collect_secrets (bool): Whether or not to remove secrets upon instance removal

            host_aliases (list[Any]): HostAliases for app containers

            hostname (str): (Deprecated) The hostname of the instance

            image (str): Registry path to the application container to use

            image_pull_policy (str): The image pull policy

            image_pull_secret (str): (Deprecated) Image pull secret for app and database containers

            image_pull_secrets (list[Any]): Image pull secrets for app and database containers

            image_version (str): Application container image version to use

            ingress_annotations (str): Annotations to add to the Ingress Controller

            ingress_api_version (str): The Ingress API version to use

            ingress_class_name (str): The name of ingress class to use instead of the cluster default.

            ingress_controller (str): Special configuration for specific Ingress Controllers

            ingress_hosts (list[Any]): Ingress hostnames of the instance

            ingress_path (str): The ingress path used to reach the deployed service

            ingress_path_type (str): The ingress path type for the deployed service

            ingress_tls_secret (str): (Deprecated) Secret where the Ingress TLS secret can be found

            ingress_type (str): The ingress type to use to reach the deployed instance

            init_container_extra_commands (str): Extra commands for the init container

            init_container_extra_volume_mounts (str): Specify volume mounts to be added to the init container

            init_container_image (str): Registry path to the init container to use

            init_container_image_version (str): Init container image version to use

            init_container_resource_requirements (dict[str, Any]): Resource requirements for the init container

            init_projects_container_image (str): Registry path to the init projects container to use

            ipv6_disabled (bool): Disable web container's nginx ipv6 listener

            ldap_cacert_secret (str): Secret where can be found the LDAP trusted Certificate Authority
              Bundle

            ldap_password_secret (str): Secret where can be found the LDAP bind password

            loadbalancer_class (str): Class of LoadBalancer to use

            loadbalancer_ip (str): Assign LoadBalancer IP address

            loadbalancer_port (int): Port to use for the loadbalancer

            loadbalancer_protocol (str): Protocol to use for the loadbalancer

            metrics_utility_configmap (str): Metrics-Utility ConfigMap

            metrics_utility_console_enabled (bool): Enable metrics utility shipping to Red Hat Hybrid Cloud Console

            metrics_utility_cronjob_gather_schedule (str): Metrics-Utility Gather Data CronJob Schedule

            metrics_utility_cronjob_report_schedule (str): Metrics-Utility Report CronJob Schedule

            metrics_utility_enabled (bool): Enable metrics utility

            metrics_utility_image (str): Metrics-Utility Image

            metrics_utility_image_pull_policy (str): Metrics-Utility Image PullPolicy

            metrics_utility_image_version (str): Metrics-Utility Image Version

            metrics_utility_pvc_claim (str): Metrics-Utility PVC Claim

            metrics_utility_pvc_claim_size (str): Metrics-Utility PVC Claim Size

            metrics_utility_pvc_claim_storage_class (str): Metrics-Utility PVC Claim Storage Class

            metrics_utility_secret (str): Metrics-Utility Secret

            metrics_utility_ship_target (str): Metrics-Utility Ship Target

            nginx_listen_queue_size (int): Set the socket listen queue size for nginx (defaults to same as uwsgi)

            nginx_worker_connections (int): Set the number of connections per worker for nginx

            nginx_worker_cpu_affinity (str): Set the CPU affinity for nginx workers

            nginx_worker_processes (int): Set the number of workers for nginx

            no_log (bool): Configure no_log for no_log tasks

            spec_node_selector (str): nodeSelector for the pods

            nodeport_port (int): Port to use for the nodeport

            old_postgres_configuration_secret (str): Secret where the old database configuration can be found for data
              migration

            postgres_configuration_secret (str): Secret where the database configuration can be found

            postgres_data_volume_init (bool): Sets permissions on the /var/lib/pgdata/data for postgres container
              using an init container (not Openshift)

            postgres_extra_args (list[Any]): No field description from API

            postgres_extra_volume_mounts (str): Specify volume mounts to be added to Postgres container

            postgres_extra_volumes (str): Specify extra volumes to add to the application pod

            postgres_image (str): Registry path to the PostgreSQL container to use

            postgres_image_version (str): PostgreSQL container image version to use

            postgres_init_container_commands (str): Customize the postgres init container commands (Non Openshift)

            postgres_init_container_resource_requirements (dict[str, Any]): (Deprecated, use postgres_resource_requirements parameter) Resource
              requirements for the postgres init container

            postgres_keep_pvc_after_upgrade (bool): Specify whether or not to keep the old PVC after PostgreSQL upgrades

            postgres_keepalives (bool): Controls whether client-side TCP keepalives are used for Postgres
              connections.

            postgres_keepalives_count (int): Controls the number of TCP keepalives that can be lost before the
              client's connection to the server is considered dead.

            postgres_keepalives_idle (int): Controls the number of seconds of inactivity after which TCP should
              send a keepalive message to the server.

            postgres_keepalives_interval (int): Controls the number of seconds after which a TCP keepalive message
              that is not acknowledged by the server should be retransmitted.

            postgres_label_selector (str): Label selector used to identify postgres pod for data migration

            postgres_priority_class (str): Assign a preexisting priority class to the postgres pod

            postgres_resource_requirements (dict[str, Any]): Resource requirements for the PostgreSQL container

            postgres_security_context_settings (dict[str, Any]): Key/values that will be set under the pod-level securityContext field

            postgres_selector (str): nodeSelector for the Postgres pods

            postgres_storage_class (str): Storage class to use for the PostgreSQL PVC

            postgres_storage_requirements (dict[str, Any]): Storage requirements for the PostgreSQL container

            postgres_tolerations (str): node tolerations for the Postgres pods

            projects_existing_claim (str): PersistentVolumeClaim to mount /var/lib/projects directory

            projects_persistence (bool): Whether or not the /var/lib/projects directory will be persistent

            projects_storage_access_mode (str): AccessMode for the /var/lib/projects PersistentVolumeClaim

            projects_storage_class (str): Storage class for the /var/lib/projects PersistentVolumeClaim

            projects_storage_size (str): Size for the /var/lib/projects PersistentVolumeClaim

            projects_use_existing_claim (str): Using existing PersistentVolumeClaim

            receptor_log_level (str): Set log level of receptor service

            redis_capabilities (list[Any]): Redis container capabilities

            redis_image (str): Registry path to the redis container to use

            redis_image_version (str): Redis container image version to use

            redis_resource_requirements (dict[str, Any]): Resource requirements for the redis container

            replicas (int): Number of instance replicas

            route_api_version (str): The route API version to use

            route_host (str): The DNS to use to points to the instance

            route_tls_secret (str): Secret where the TLS related credentials are stored

            route_tls_termination_mechanism (str): The secure TLS termination mechanism to use

            rsyslog_args (list[Any]): No field description from API

            rsyslog_command (list[Any]): No field description from API

            rsyslog_extra_env (str): No field description from API

            rsyslog_extra_volume_mounts (str): Specify volume mounts to be added to the Rsyslog container

            rsyslog_resource_requirements (dict[str, Any]): Resource requirements for the rsyslog container

            secret_key_secret (str): Secret where the secret key can be found

            security_context_settings (dict[str, Any]): Key/values that will be set under the pod-level securityContext field

            service_account_annotations (str): ServiceAccount annotations

            service_annotations (str): Annotations to add to the service

            service_labels (str): Additional labels to apply to the service

            service_type (str): The service type to be used on the deployed instance

            session_cookie_secure (str): Set session cookie secure mode for web

            set_self_labels (bool): Maintain some of the recommended `app.kubernetes.io/*` labels on the
              resource (self)

            task_affinity (dict[str, Any]): If specified, the pod's scheduling constraints

            task_annotations (str): Task deployment annotations. This will override the general
              annotations parameter for the Task deployment.

            task_args (list[Any]): No field description from API

            task_command (list[Any]): No field description from API

            task_extra_env (str): No field description from API

            task_extra_volume_mounts (str): Specify volume mounts to be added to Task container

            task_liveness_failure_threshold (int): Number of consecutive failure events to identify failure of task pod

            task_liveness_initial_delay (int): Initial delay before starting liveness checks on task pod

            task_liveness_period (int): Time period in seconds between each liveness check for the task pod

            task_liveness_timeout (int): Number of seconds to wait for a probe response from task pod

            task_manage_replicas (bool): Enables operator control of replicas count for the task deployment
              when set to 'true'

            task_node_selector (str): nodeSelector for the task pods

            task_privileged (bool): If a privileged security context should be enabled

            task_readiness_failure_threshold (int): Number of consecutive failure events to identify failure of task pod

            task_readiness_initial_delay (int): Initial delay before starting readiness checks on task pod

            task_readiness_period (int): Time period in seconds between each readiness check for the task pod

            task_readiness_timeout (int): Number of seconds to wait for a probe response from task pod

            task_replicas (int): Number of task instance replicas

            task_resource_requirements (dict[str, Any]): Resource requirements for the task container

            task_tolerations (str): node tolerations for the task pods

            task_topology_spread_constraints (str): topology rule(s) for the task pods

            termination_grace_period_seconds (int): Optional duration in seconds pods needs to terminate gracefully

            tolerations (str): node tolerations for the pods

            topology_spread_constraints (str): topology rule(s) for the pods

            uwsgi_listen_queue_size (int): Set the socket listen queue size for uwsgi

            uwsgi_processes (int): Set the number of uwsgi processes to run in a web container

            web_affinity (dict[str, Any]): If specified, the pod's scheduling constraints

            web_annotations (str): Web deployment annotations. This will override the general annotations
              parameter for the Web deployment.

            web_args (list[Any]): No field description from API

            web_command (list[Any]): No field description from API

            web_extra_env (str): No field description from API

            web_extra_volume_mounts (str): Specify volume mounts to be added to the Web container

            web_liveness_failure_threshold (int): Number of consecutive failure events to identify failure of web pod

            web_liveness_initial_delay (int): Initial delay before starting liveness checks on web pod

            web_liveness_period (int): Time period in seconds between each liveness check for the web pod

            web_liveness_timeout (int): Number of seconds to wait for a probe response from web pod

            web_manage_replicas (bool): Enables operator control of replicas count for the web deployment when
              set to 'true'

            web_node_selector (str): nodeSelector for the web pods

            web_readiness_failure_threshold (int): Number of consecutive failure events to identify failure of web pod

            web_readiness_initial_delay (int): Initial delay before starting readiness checks on web pod

            web_readiness_period (int): Time period in seconds between each readiness check for the web pod

            web_readiness_timeout (int): Number of seconds to wait for a probe response from web pod

            web_replicas (int): Number of web instance replicas

            web_resource_requirements (dict[str, Any]): Resource requirements for the web container

            web_tolerations (str): node tolerations for the web pods

            web_topology_spread_constraints (str): topology rule(s) for the web pods

        """
        super().__init__(**kwargs)

        self.additional_labels = additional_labels
        self.admin_email = admin_email
        self.admin_password_secret = admin_password_secret
        self.admin_user = admin_user
        self.affinity = affinity
        self.spec_annotations = spec_annotations
        self.api_urlpattern_prefix = api_urlpattern_prefix
        self.spec_api_version = spec_api_version
        self.auto_upgrade = auto_upgrade
        self.broadcast_websocket_secret = broadcast_websocket_secret
        self.bundle_cacert_secret = bundle_cacert_secret
        self.ca_trust_bundle = ca_trust_bundle
        self.control_plane_ee_image = control_plane_ee_image
        self.control_plane_priority_class = control_plane_priority_class
        self.create_preload_data = create_preload_data
        self.csrf_cookie_secure = csrf_cookie_secure
        self.deployment_type = deployment_type
        self.development_mode = development_mode
        self.ee_extra_env = ee_extra_env
        self.ee_extra_volume_mounts = ee_extra_volume_mounts
        self.ee_images = ee_images
        self.ee_pull_credentials_secret = ee_pull_credentials_secret
        self.ee_resource_requirements = ee_resource_requirements
        self.extra_settings = extra_settings
        self.extra_settings_files = extra_settings_files
        self.extra_volumes = extra_volumes
        self.garbage_collect_secrets = garbage_collect_secrets
        self.host_aliases = host_aliases
        self.hostname = hostname
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.image_pull_secret = image_pull_secret
        self.image_pull_secrets = image_pull_secrets
        self.image_version = image_version
        self.ingress_annotations = ingress_annotations
        self.ingress_api_version = ingress_api_version
        self.ingress_class_name = ingress_class_name
        self.ingress_controller = ingress_controller
        self.ingress_hosts = ingress_hosts
        self.ingress_path = ingress_path
        self.ingress_path_type = ingress_path_type
        self.ingress_tls_secret = ingress_tls_secret
        self.ingress_type = ingress_type
        self.init_container_extra_commands = init_container_extra_commands
        self.init_container_extra_volume_mounts = init_container_extra_volume_mounts
        self.init_container_image = init_container_image
        self.init_container_image_version = init_container_image_version
        self.init_container_resource_requirements = init_container_resource_requirements
        self.init_projects_container_image = init_projects_container_image
        self.ipv6_disabled = ipv6_disabled
        self.ldap_cacert_secret = ldap_cacert_secret
        self.ldap_password_secret = ldap_password_secret
        self.loadbalancer_class = loadbalancer_class
        self.loadbalancer_ip = loadbalancer_ip
        self.loadbalancer_port = loadbalancer_port
        self.loadbalancer_protocol = loadbalancer_protocol
        self.metrics_utility_configmap = metrics_utility_configmap
        self.metrics_utility_console_enabled = metrics_utility_console_enabled
        self.metrics_utility_cronjob_gather_schedule = metrics_utility_cronjob_gather_schedule
        self.metrics_utility_cronjob_report_schedule = metrics_utility_cronjob_report_schedule
        self.metrics_utility_enabled = metrics_utility_enabled
        self.metrics_utility_image = metrics_utility_image
        self.metrics_utility_image_pull_policy = metrics_utility_image_pull_policy
        self.metrics_utility_image_version = metrics_utility_image_version
        self.metrics_utility_pvc_claim = metrics_utility_pvc_claim
        self.metrics_utility_pvc_claim_size = metrics_utility_pvc_claim_size
        self.metrics_utility_pvc_claim_storage_class = metrics_utility_pvc_claim_storage_class
        self.metrics_utility_secret = metrics_utility_secret
        self.metrics_utility_ship_target = metrics_utility_ship_target
        self.nginx_listen_queue_size = nginx_listen_queue_size
        self.nginx_worker_connections = nginx_worker_connections
        self.nginx_worker_cpu_affinity = nginx_worker_cpu_affinity
        self.nginx_worker_processes = nginx_worker_processes
        self.no_log = no_log
        self.spec_node_selector = spec_node_selector
        self.nodeport_port = nodeport_port
        self.old_postgres_configuration_secret = old_postgres_configuration_secret
        self.postgres_configuration_secret = postgres_configuration_secret
        self.postgres_data_volume_init = postgres_data_volume_init
        self.postgres_extra_args = postgres_extra_args
        self.postgres_extra_volume_mounts = postgres_extra_volume_mounts
        self.postgres_extra_volumes = postgres_extra_volumes
        self.postgres_image = postgres_image
        self.postgres_image_version = postgres_image_version
        self.postgres_init_container_commands = postgres_init_container_commands
        self.postgres_init_container_resource_requirements = postgres_init_container_resource_requirements
        self.postgres_keep_pvc_after_upgrade = postgres_keep_pvc_after_upgrade
        self.postgres_keepalives = postgres_keepalives
        self.postgres_keepalives_count = postgres_keepalives_count
        self.postgres_keepalives_idle = postgres_keepalives_idle
        self.postgres_keepalives_interval = postgres_keepalives_interval
        self.postgres_label_selector = postgres_label_selector
        self.postgres_priority_class = postgres_priority_class
        self.postgres_resource_requirements = postgres_resource_requirements
        self.postgres_security_context_settings = postgres_security_context_settings
        self.postgres_selector = postgres_selector
        self.postgres_storage_class = postgres_storage_class
        self.postgres_storage_requirements = postgres_storage_requirements
        self.postgres_tolerations = postgres_tolerations
        self.projects_existing_claim = projects_existing_claim
        self.projects_persistence = projects_persistence
        self.projects_storage_access_mode = projects_storage_access_mode
        self.projects_storage_class = projects_storage_class
        self.projects_storage_size = projects_storage_size
        self.projects_use_existing_claim = projects_use_existing_claim
        self.receptor_log_level = receptor_log_level
        self.redis_capabilities = redis_capabilities
        self.redis_image = redis_image
        self.redis_image_version = redis_image_version
        self.redis_resource_requirements = redis_resource_requirements
        self.replicas = replicas
        self.route_api_version = route_api_version
        self.route_host = route_host
        self.route_tls_secret = route_tls_secret
        self.route_tls_termination_mechanism = route_tls_termination_mechanism
        self.rsyslog_args = rsyslog_args
        self.rsyslog_command = rsyslog_command
        self.rsyslog_extra_env = rsyslog_extra_env
        self.rsyslog_extra_volume_mounts = rsyslog_extra_volume_mounts
        self.rsyslog_resource_requirements = rsyslog_resource_requirements
        self.secret_key_secret = secret_key_secret
        self.security_context_settings = security_context_settings
        self.service_account_annotations = service_account_annotations
        self.service_annotations = service_annotations
        self.service_labels = service_labels
        self.service_type = service_type
        self.session_cookie_secure = session_cookie_secure
        self.set_self_labels = set_self_labels
        self.task_affinity = task_affinity
        self.task_annotations = task_annotations
        self.task_args = task_args
        self.task_command = task_command
        self.task_extra_env = task_extra_env
        self.task_extra_volume_mounts = task_extra_volume_mounts
        self.task_liveness_failure_threshold = task_liveness_failure_threshold
        self.task_liveness_initial_delay = task_liveness_initial_delay
        self.task_liveness_period = task_liveness_period
        self.task_liveness_timeout = task_liveness_timeout
        self.task_manage_replicas = task_manage_replicas
        self.task_node_selector = task_node_selector
        self.task_privileged = task_privileged
        self.task_readiness_failure_threshold = task_readiness_failure_threshold
        self.task_readiness_initial_delay = task_readiness_initial_delay
        self.task_readiness_period = task_readiness_period
        self.task_readiness_timeout = task_readiness_timeout
        self.task_replicas = task_replicas
        self.task_resource_requirements = task_resource_requirements
        self.task_tolerations = task_tolerations
        self.task_topology_spread_constraints = task_topology_spread_constraints
        self.termination_grace_period_seconds = termination_grace_period_seconds
        self.tolerations = tolerations
        self.topology_spread_constraints = topology_spread_constraints
        self.uwsgi_listen_queue_size = uwsgi_listen_queue_size
        self.uwsgi_processes = uwsgi_processes
        self.web_affinity = web_affinity
        self.web_annotations = web_annotations
        self.web_args = web_args
        self.web_command = web_command
        self.web_extra_env = web_extra_env
        self.web_extra_volume_mounts = web_extra_volume_mounts
        self.web_liveness_failure_threshold = web_liveness_failure_threshold
        self.web_liveness_initial_delay = web_liveness_initial_delay
        self.web_liveness_period = web_liveness_period
        self.web_liveness_timeout = web_liveness_timeout
        self.web_manage_replicas = web_manage_replicas
        self.web_node_selector = web_node_selector
        self.web_readiness_failure_threshold = web_readiness_failure_threshold
        self.web_readiness_initial_delay = web_readiness_initial_delay
        self.web_readiness_period = web_readiness_period
        self.web_readiness_timeout = web_readiness_timeout
        self.web_replicas = web_replicas
        self.web_resource_requirements = web_resource_requirements
        self.web_tolerations = web_tolerations
        self.web_topology_spread_constraints = web_topology_spread_constraints

    def to_dict(self) -> None:

        super().to_dict()

        if not self.kind_dict and not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.additional_labels is not None:
                _spec["additional_labels"] = self.additional_labels

            if self.admin_email is not None:
                _spec["admin_email"] = self.admin_email

            if self.admin_password_secret is not None:
                _spec["admin_password_secret"] = self.admin_password_secret

            if self.admin_user is not None:
                _spec["admin_user"] = self.admin_user

            if self.affinity is not None:
                _spec["affinity"] = self.affinity

            if self.spec_annotations is not None:
                _spec["annotations"] = self.spec_annotations

            if self.api_urlpattern_prefix is not None:
                _spec["api_urlpattern_prefix"] = self.api_urlpattern_prefix

            if self.spec_api_version is not None:
                _spec["api_version"] = self.spec_api_version

            if self.auto_upgrade is not None:
                _spec["auto_upgrade"] = self.auto_upgrade

            if self.broadcast_websocket_secret is not None:
                _spec["broadcast_websocket_secret"] = self.broadcast_websocket_secret

            if self.bundle_cacert_secret is not None:
                _spec["bundle_cacert_secret"] = self.bundle_cacert_secret

            if self.ca_trust_bundle is not None:
                _spec["ca_trust_bundle"] = self.ca_trust_bundle

            if self.control_plane_ee_image is not None:
                _spec["control_plane_ee_image"] = self.control_plane_ee_image

            if self.control_plane_priority_class is not None:
                _spec["control_plane_priority_class"] = self.control_plane_priority_class

            if self.create_preload_data is not None:
                _spec["create_preload_data"] = self.create_preload_data

            if self.csrf_cookie_secure is not None:
                _spec["csrf_cookie_secure"] = self.csrf_cookie_secure

            if self.deployment_type is not None:
                _spec["deployment_type"] = self.deployment_type

            if self.development_mode is not None:
                _spec["development_mode"] = self.development_mode

            if self.ee_extra_env is not None:
                _spec["ee_extra_env"] = self.ee_extra_env

            if self.ee_extra_volume_mounts is not None:
                _spec["ee_extra_volume_mounts"] = self.ee_extra_volume_mounts

            if self.ee_images is not None:
                _spec["ee_images"] = self.ee_images

            if self.ee_pull_credentials_secret is not None:
                _spec["ee_pull_credentials_secret"] = self.ee_pull_credentials_secret

            if self.ee_resource_requirements is not None:
                _spec["ee_resource_requirements"] = self.ee_resource_requirements

            if self.extra_settings is not None:
                _spec["extra_settings"] = self.extra_settings

            if self.extra_settings_files is not None:
                _spec["extra_settings_files"] = self.extra_settings_files

            if self.extra_volumes is not None:
                _spec["extra_volumes"] = self.extra_volumes

            if self.garbage_collect_secrets is not None:
                _spec["garbage_collect_secrets"] = self.garbage_collect_secrets

            if self.host_aliases is not None:
                _spec["host_aliases"] = self.host_aliases

            if self.hostname is not None:
                _spec["hostname"] = self.hostname

            if self.image is not None:
                _spec["image"] = self.image

            if self.image_pull_policy is not None:
                _spec["image_pull_policy"] = self.image_pull_policy

            if self.image_pull_secret is not None:
                _spec["image_pull_secret"] = self.image_pull_secret

            if self.image_pull_secrets is not None:
                _spec["image_pull_secrets"] = self.image_pull_secrets

            if self.image_version is not None:
                _spec["image_version"] = self.image_version

            if self.ingress_annotations is not None:
                _spec["ingress_annotations"] = self.ingress_annotations

            if self.ingress_api_version is not None:
                _spec["ingress_api_version"] = self.ingress_api_version

            if self.ingress_class_name is not None:
                _spec["ingress_class_name"] = self.ingress_class_name

            if self.ingress_controller is not None:
                _spec["ingress_controller"] = self.ingress_controller

            if self.ingress_hosts is not None:
                _spec["ingress_hosts"] = self.ingress_hosts

            if self.ingress_path is not None:
                _spec["ingress_path"] = self.ingress_path

            if self.ingress_path_type is not None:
                _spec["ingress_path_type"] = self.ingress_path_type

            if self.ingress_tls_secret is not None:
                _spec["ingress_tls_secret"] = self.ingress_tls_secret

            if self.ingress_type is not None:
                _spec["ingress_type"] = self.ingress_type

            if self.init_container_extra_commands is not None:
                _spec["init_container_extra_commands"] = self.init_container_extra_commands

            if self.init_container_extra_volume_mounts is not None:
                _spec["init_container_extra_volume_mounts"] = self.init_container_extra_volume_mounts

            if self.init_container_image is not None:
                _spec["init_container_image"] = self.init_container_image

            if self.init_container_image_version is not None:
                _spec["init_container_image_version"] = self.init_container_image_version

            if self.init_container_resource_requirements is not None:
                _spec["init_container_resource_requirements"] = self.init_container_resource_requirements

            if self.init_projects_container_image is not None:
                _spec["init_projects_container_image"] = self.init_projects_container_image

            if self.ipv6_disabled is not None:
                _spec["ipv6_disabled"] = self.ipv6_disabled

            if self.ldap_cacert_secret is not None:
                _spec["ldap_cacert_secret"] = self.ldap_cacert_secret

            if self.ldap_password_secret is not None:
                _spec["ldap_password_secret"] = self.ldap_password_secret

            if self.loadbalancer_class is not None:
                _spec["loadbalancer_class"] = self.loadbalancer_class

            if self.loadbalancer_ip is not None:
                _spec["loadbalancer_ip"] = self.loadbalancer_ip

            if self.loadbalancer_port is not None:
                _spec["loadbalancer_port"] = self.loadbalancer_port

            if self.loadbalancer_protocol is not None:
                _spec["loadbalancer_protocol"] = self.loadbalancer_protocol

            if self.metrics_utility_configmap is not None:
                _spec["metrics_utility_configmap"] = self.metrics_utility_configmap

            if self.metrics_utility_console_enabled is not None:
                _spec["metrics_utility_console_enabled"] = self.metrics_utility_console_enabled

            if self.metrics_utility_cronjob_gather_schedule is not None:
                _spec["metrics_utility_cronjob_gather_schedule"] = self.metrics_utility_cronjob_gather_schedule

            if self.metrics_utility_cronjob_report_schedule is not None:
                _spec["metrics_utility_cronjob_report_schedule"] = self.metrics_utility_cronjob_report_schedule

            if self.metrics_utility_enabled is not None:
                _spec["metrics_utility_enabled"] = self.metrics_utility_enabled

            if self.metrics_utility_image is not None:
                _spec["metrics_utility_image"] = self.metrics_utility_image

            if self.metrics_utility_image_pull_policy is not None:
                _spec["metrics_utility_image_pull_policy"] = self.metrics_utility_image_pull_policy

            if self.metrics_utility_image_version is not None:
                _spec["metrics_utility_image_version"] = self.metrics_utility_image_version

            if self.metrics_utility_pvc_claim is not None:
                _spec["metrics_utility_pvc_claim"] = self.metrics_utility_pvc_claim

            if self.metrics_utility_pvc_claim_size is not None:
                _spec["metrics_utility_pvc_claim_size"] = self.metrics_utility_pvc_claim_size

            if self.metrics_utility_pvc_claim_storage_class is not None:
                _spec["metrics_utility_pvc_claim_storage_class"] = self.metrics_utility_pvc_claim_storage_class

            if self.metrics_utility_secret is not None:
                _spec["metrics_utility_secret"] = self.metrics_utility_secret

            if self.metrics_utility_ship_target is not None:
                _spec["metrics_utility_ship_target"] = self.metrics_utility_ship_target

            if self.nginx_listen_queue_size is not None:
                _spec["nginx_listen_queue_size"] = self.nginx_listen_queue_size

            if self.nginx_worker_connections is not None:
                _spec["nginx_worker_connections"] = self.nginx_worker_connections

            if self.nginx_worker_cpu_affinity is not None:
                _spec["nginx_worker_cpu_affinity"] = self.nginx_worker_cpu_affinity

            if self.nginx_worker_processes is not None:
                _spec["nginx_worker_processes"] = self.nginx_worker_processes

            if self.no_log is not None:
                _spec["no_log"] = self.no_log

            if self.spec_node_selector is not None:
                _spec["node_selector"] = self.spec_node_selector

            if self.nodeport_port is not None:
                _spec["nodeport_port"] = self.nodeport_port

            if self.old_postgres_configuration_secret is not None:
                _spec["old_postgres_configuration_secret"] = self.old_postgres_configuration_secret

            if self.postgres_configuration_secret is not None:
                _spec["postgres_configuration_secret"] = self.postgres_configuration_secret

            if self.postgres_data_volume_init is not None:
                _spec["postgres_data_volume_init"] = self.postgres_data_volume_init

            if self.postgres_extra_args is not None:
                _spec["postgres_extra_args"] = self.postgres_extra_args

            if self.postgres_extra_volume_mounts is not None:
                _spec["postgres_extra_volume_mounts"] = self.postgres_extra_volume_mounts

            if self.postgres_extra_volumes is not None:
                _spec["postgres_extra_volumes"] = self.postgres_extra_volumes

            if self.postgres_image is not None:
                _spec["postgres_image"] = self.postgres_image

            if self.postgres_image_version is not None:
                _spec["postgres_image_version"] = self.postgres_image_version

            if self.postgres_init_container_commands is not None:
                _spec["postgres_init_container_commands"] = self.postgres_init_container_commands

            if self.postgres_init_container_resource_requirements is not None:
                _spec["postgres_init_container_resource_requirements"] = (
                    self.postgres_init_container_resource_requirements
                )

            if self.postgres_keep_pvc_after_upgrade is not None:
                _spec["postgres_keep_pvc_after_upgrade"] = self.postgres_keep_pvc_after_upgrade

            if self.postgres_keepalives is not None:
                _spec["postgres_keepalives"] = self.postgres_keepalives

            if self.postgres_keepalives_count is not None:
                _spec["postgres_keepalives_count"] = self.postgres_keepalives_count

            if self.postgres_keepalives_idle is not None:
                _spec["postgres_keepalives_idle"] = self.postgres_keepalives_idle

            if self.postgres_keepalives_interval is not None:
                _spec["postgres_keepalives_interval"] = self.postgres_keepalives_interval

            if self.postgres_label_selector is not None:
                _spec["postgres_label_selector"] = self.postgres_label_selector

            if self.postgres_priority_class is not None:
                _spec["postgres_priority_class"] = self.postgres_priority_class

            if self.postgres_resource_requirements is not None:
                _spec["postgres_resource_requirements"] = self.postgres_resource_requirements

            if self.postgres_security_context_settings is not None:
                _spec["postgres_security_context_settings"] = self.postgres_security_context_settings

            if self.postgres_selector is not None:
                _spec["postgres_selector"] = self.postgres_selector

            if self.postgres_storage_class is not None:
                _spec["postgres_storage_class"] = self.postgres_storage_class

            if self.postgres_storage_requirements is not None:
                _spec["postgres_storage_requirements"] = self.postgres_storage_requirements

            if self.postgres_tolerations is not None:
                _spec["postgres_tolerations"] = self.postgres_tolerations

            if self.projects_existing_claim is not None:
                _spec["projects_existing_claim"] = self.projects_existing_claim

            if self.projects_persistence is not None:
                _spec["projects_persistence"] = self.projects_persistence

            if self.projects_storage_access_mode is not None:
                _spec["projects_storage_access_mode"] = self.projects_storage_access_mode

            if self.projects_storage_class is not None:
                _spec["projects_storage_class"] = self.projects_storage_class

            if self.projects_storage_size is not None:
                _spec["projects_storage_size"] = self.projects_storage_size

            if self.projects_use_existing_claim is not None:
                _spec["projects_use_existing_claim"] = self.projects_use_existing_claim

            if self.receptor_log_level is not None:
                _spec["receptor_log_level"] = self.receptor_log_level

            if self.redis_capabilities is not None:
                _spec["redis_capabilities"] = self.redis_capabilities

            if self.redis_image is not None:
                _spec["redis_image"] = self.redis_image

            if self.redis_image_version is not None:
                _spec["redis_image_version"] = self.redis_image_version

            if self.redis_resource_requirements is not None:
                _spec["redis_resource_requirements"] = self.redis_resource_requirements

            if self.replicas is not None:
                _spec["replicas"] = self.replicas

            if self.route_api_version is not None:
                _spec["route_api_version"] = self.route_api_version

            if self.route_host is not None:
                _spec["route_host"] = self.route_host

            if self.route_tls_secret is not None:
                _spec["route_tls_secret"] = self.route_tls_secret

            if self.route_tls_termination_mechanism is not None:
                _spec["route_tls_termination_mechanism"] = self.route_tls_termination_mechanism

            if self.rsyslog_args is not None:
                _spec["rsyslog_args"] = self.rsyslog_args

            if self.rsyslog_command is not None:
                _spec["rsyslog_command"] = self.rsyslog_command

            if self.rsyslog_extra_env is not None:
                _spec["rsyslog_extra_env"] = self.rsyslog_extra_env

            if self.rsyslog_extra_volume_mounts is not None:
                _spec["rsyslog_extra_volume_mounts"] = self.rsyslog_extra_volume_mounts

            if self.rsyslog_resource_requirements is not None:
                _spec["rsyslog_resource_requirements"] = self.rsyslog_resource_requirements

            if self.secret_key_secret is not None:
                _spec["secret_key_secret"] = self.secret_key_secret

            if self.security_context_settings is not None:
                _spec["security_context_settings"] = self.security_context_settings

            if self.service_account_annotations is not None:
                _spec["service_account_annotations"] = self.service_account_annotations

            if self.service_annotations is not None:
                _spec["service_annotations"] = self.service_annotations

            if self.service_labels is not None:
                _spec["service_labels"] = self.service_labels

            if self.service_type is not None:
                _spec["service_type"] = self.service_type

            if self.session_cookie_secure is not None:
                _spec["session_cookie_secure"] = self.session_cookie_secure

            if self.set_self_labels is not None:
                _spec["set_self_labels"] = self.set_self_labels

            if self.task_affinity is not None:
                _spec["task_affinity"] = self.task_affinity

            if self.task_annotations is not None:
                _spec["task_annotations"] = self.task_annotations

            if self.task_args is not None:
                _spec["task_args"] = self.task_args

            if self.task_command is not None:
                _spec["task_command"] = self.task_command

            if self.task_extra_env is not None:
                _spec["task_extra_env"] = self.task_extra_env

            if self.task_extra_volume_mounts is not None:
                _spec["task_extra_volume_mounts"] = self.task_extra_volume_mounts

            if self.task_liveness_failure_threshold is not None:
                _spec["task_liveness_failure_threshold"] = self.task_liveness_failure_threshold

            if self.task_liveness_initial_delay is not None:
                _spec["task_liveness_initial_delay"] = self.task_liveness_initial_delay

            if self.task_liveness_period is not None:
                _spec["task_liveness_period"] = self.task_liveness_period

            if self.task_liveness_timeout is not None:
                _spec["task_liveness_timeout"] = self.task_liveness_timeout

            if self.task_manage_replicas is not None:
                _spec["task_manage_replicas"] = self.task_manage_replicas

            if self.task_node_selector is not None:
                _spec["task_node_selector"] = self.task_node_selector

            if self.task_privileged is not None:
                _spec["task_privileged"] = self.task_privileged

            if self.task_readiness_failure_threshold is not None:
                _spec["task_readiness_failure_threshold"] = self.task_readiness_failure_threshold

            if self.task_readiness_initial_delay is not None:
                _spec["task_readiness_initial_delay"] = self.task_readiness_initial_delay

            if self.task_readiness_period is not None:
                _spec["task_readiness_period"] = self.task_readiness_period

            if self.task_readiness_timeout is not None:
                _spec["task_readiness_timeout"] = self.task_readiness_timeout

            if self.task_replicas is not None:
                _spec["task_replicas"] = self.task_replicas

            if self.task_resource_requirements is not None:
                _spec["task_resource_requirements"] = self.task_resource_requirements

            if self.task_tolerations is not None:
                _spec["task_tolerations"] = self.task_tolerations

            if self.task_topology_spread_constraints is not None:
                _spec["task_topology_spread_constraints"] = self.task_topology_spread_constraints

            if self.termination_grace_period_seconds is not None:
                _spec["termination_grace_period_seconds"] = self.termination_grace_period_seconds

            if self.tolerations is not None:
                _spec["tolerations"] = self.tolerations

            if self.topology_spread_constraints is not None:
                _spec["topology_spread_constraints"] = self.topology_spread_constraints

            if self.uwsgi_listen_queue_size is not None:
                _spec["uwsgi_listen_queue_size"] = self.uwsgi_listen_queue_size

            if self.uwsgi_processes is not None:
                _spec["uwsgi_processes"] = self.uwsgi_processes

            if self.web_affinity is not None:
                _spec["web_affinity"] = self.web_affinity

            if self.web_annotations is not None:
                _spec["web_annotations"] = self.web_annotations

            if self.web_args is not None:
                _spec["web_args"] = self.web_args

            if self.web_command is not None:
                _spec["web_command"] = self.web_command

            if self.web_extra_env is not None:
                _spec["web_extra_env"] = self.web_extra_env

            if self.web_extra_volume_mounts is not None:
                _spec["web_extra_volume_mounts"] = self.web_extra_volume_mounts

            if self.web_liveness_failure_threshold is not None:
                _spec["web_liveness_failure_threshold"] = self.web_liveness_failure_threshold

            if self.web_liveness_initial_delay is not None:
                _spec["web_liveness_initial_delay"] = self.web_liveness_initial_delay

            if self.web_liveness_period is not None:
                _spec["web_liveness_period"] = self.web_liveness_period

            if self.web_liveness_timeout is not None:
                _spec["web_liveness_timeout"] = self.web_liveness_timeout

            if self.web_manage_replicas is not None:
                _spec["web_manage_replicas"] = self.web_manage_replicas

            if self.web_node_selector is not None:
                _spec["web_node_selector"] = self.web_node_selector

            if self.web_readiness_failure_threshold is not None:
                _spec["web_readiness_failure_threshold"] = self.web_readiness_failure_threshold

            if self.web_readiness_initial_delay is not None:
                _spec["web_readiness_initial_delay"] = self.web_readiness_initial_delay

            if self.web_readiness_period is not None:
                _spec["web_readiness_period"] = self.web_readiness_period

            if self.web_readiness_timeout is not None:
                _spec["web_readiness_timeout"] = self.web_readiness_timeout

            if self.web_replicas is not None:
                _spec["web_replicas"] = self.web_replicas

            if self.web_resource_requirements is not None:
                _spec["web_resource_requirements"] = self.web_resource_requirements

            if self.web_tolerations is not None:
                _spec["web_tolerations"] = self.web_tolerations

            if self.web_topology_spread_constraints is not None:
                _spec["web_topology_spread_constraints"] = self.web_topology_spread_constraints

    # End of generated code
