# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, List, Optional
from ocp_resources.resource import NamespacedResource


class MariaDB(NamespacedResource):
    """
    MariaDB is the Schema for the mariadbs API. It is used to define MariaDB clusters.
    """

    api_group: str = NamespacedResource.ApiGroup.K8S_MARIADB_COM

    def __init__(
        self,
        affinity: Optional[Dict[str, Any]] = None,
        args: Optional[List[Any]] = None,
        bootstrap_from: Optional[Dict[str, Any]] = None,
        command: Optional[List[Any]] = None,
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
        node_selector: Optional[Dict[str, Any]] = None,
        password_hash_secret_key_ref: Optional[Dict[str, Any]] = None,
        password_plugin: Optional[Dict[str, Any]] = None,
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
        replicas_allow_even_number: Optional[bool] = None,
        replication: Optional[Dict[str, Any]] = None,
        resources: Optional[Dict[str, Any]] = None,
        root_empty_password: Optional[bool] = None,
        root_password_secret_key_ref: Optional[Dict[str, Any]] = None,
        secondary_connection: Optional[Dict[str, Any]] = None,
        secondary_service: Optional[Dict[str, Any]] = None,
        security_context: Optional[Dict[str, Any]] = None,
        service: Optional[Dict[str, Any]] = None,
        service_account_name: Optional[str] = "",
        service_ports: Optional[List[Any]] = None,
        sidecar_containers: Optional[List[Any]] = None,
        storage: Optional[Dict[str, Any]] = None,
        suspend: Optional[bool] = None,
        time_zone: Optional[str] = "",
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
            affinity (Dict[str, Any]): Affinity to be used in the Pod.

            args (List[Any]): Args to be used in the Container.

            bootstrap_from (Dict[str, Any]): BootstrapFrom defines a source to bootstrap from.

            command (List[Any]): Command to be used in the Container.

            connection (Dict[str, Any]): Connection defines a template to configure the general Connection
              object. This Connection provides the initial User access to the
              initial Database. It will make use of the Service to route network
              traffic to all Pods.

            database (str): Database is the name of the initial Database.

            env (List[Any]): Env represents the environment variables to be injected in a
              container.

            env_from (List[Any]): EnvFrom represents the references (via ConfigMap and Secrets) to
              environment variables to be injected in the container.

            galera (Dict[str, Any]): Replication configures high availability via Galera.

            image (str): Image name to be used by the MariaDB instances. The supported format
              is `<image>:<tag>`. Only MariaDB official images are supported.

            image_pull_policy (str): ImagePullPolicy is the image pull policy. One of `Always`, `Never` or
              `IfNotPresent`. If not defined, it defaults to `IfNotPresent`.

            image_pull_secrets (List[Any]): ImagePullSecrets is the list of pull Secrets to be used to pull the
              image.

            inherit_metadata (Dict[str, Any]): InheritMetadata defines the metadata to be inherited by children
              resources.

            init_containers (List[Any]): InitContainers to be used in the Pod.

            liveness_probe (Dict[str, Any]): LivenessProbe to be used in the Container.

            max_scale (Dict[str, Any]): MaxScale is the MaxScale specification that defines the MaxScale
              resource to be used with the current MariaDB. When enabling this
              field, MaxScaleRef is automatically set.

            max_scale_ref (Dict[str, Any]): MaxScaleRef is a reference to a MaxScale resource to be used with the
              current MariaDB. Providing this field implies delegating high
              availability tasks such as primary failover to MaxScale.

            metrics (Dict[str, Any]): Metrics configures metrics and how to scrape them.

            my_cnf (str): MyCnf allows to specify the my.cnf file mounted by Mariadb. Updating
              this field will trigger an update to the Mariadb resource.

            my_cnf_config_map_key_ref (Dict[str, Any]): MyCnfConfigMapKeyRef is a reference to the my.cnf config file provided
              via a ConfigMap. If not provided, it will be defaulted with a
              reference to a ConfigMap containing the MyCnf field. If the
              referred ConfigMap is labeled with "k8s.mariadb.com/watch", an
              update to the Mariadb resource will be triggered when the
              ConfigMap is updated.

            node_selector (Dict[str, Any]): NodeSelector to be used in the Pod.

            password_hash_secret_key_ref (Dict[str, Any]): PasswordHashSecretKeyRef is a reference to the password hash to be
              used by the initial User. If the referred Secret is labeled with
              "k8s.mariadb.com/watch", updates may be performed to the Secret in
              order to update the password hash.

            password_plugin (Dict[str, Any]): PasswordPlugin is a reference to the password plugin and arguments to
              be used by the initial User.

            password_secret_key_ref (Dict[str, Any]): PasswordSecretKeyRef is a reference to a Secret that contains the
              password to be used by the initial User. If the referred Secret is
              labeled with "k8s.mariadb.com/watch", updates may be performed to
              the Secret in order to update the password.

            pod_disruption_budget (Dict[str, Any]): PodDisruptionBudget defines the budget for replica availability.

            pod_metadata (Dict[str, Any]): PodMetadata defines extra metadata for the Pod.

            pod_security_context (Dict[str, Any]): SecurityContext holds pod-level security attributes and common
              container settings.

            port (int): Port where the instances will be listening for connections.

            primary_connection (Dict[str, Any]): PrimaryConnection defines a template to configure the primary
              Connection object. This Connection provides the initial User
              access to the initial Database. It will make use of the
              PrimaryService to route network traffic to the primary Pod.

            primary_service (Dict[str, Any]): PrimaryService defines a template to configure the primary Service
              object. The network traffic of this Service will be routed to the
              primary Pod.

            priority_class_name (str): PriorityClassName to be used in the Pod.

            readiness_probe (Dict[str, Any]): ReadinessProbe to be used in the Container.

            replicas (int): Replicas indicates the number of desired instances.

            replicas_allow_even_number (bool): disables the validation check for an odd number of replicas.

            replication (Dict[str, Any]): Replication configures high availability via replication. This feature
              is still in alpha, use Galera if you are looking for a more
              production-ready HA.

            resources (Dict[str, Any]): Resouces describes the compute resource requirements.

            root_empty_password (bool): RootEmptyPassword indicates if the root password should be empty.
              Don't use this feature in production, it is only intended for
              development and test environments.

            root_password_secret_key_ref (Dict[str, Any]): RootPasswordSecretKeyRef is a reference to a Secret key containing the
              root password.

            secondary_connection (Dict[str, Any]): SecondaryConnection defines a template to configure the secondary
              Connection object. This Connection provides the initial User
              access to the initial Database. It will make use of the
              SecondaryService to route network traffic to the secondary Pods.

            secondary_service (Dict[str, Any]): SecondaryService defines a template to configure the secondary Service
              object. The network traffic of this Service will be routed to the
              secondary Pods.

            security_context (Dict[str, Any]): SecurityContext holds security configuration that will be applied to a
              container.

            service (Dict[str, Any]): Service defines a template to configure the general Service object.
              The network traffic of this Service will be routed to all Pods.

            service_account_name (str): ServiceAccountName is the name of the ServiceAccount to be used by the
              Pods.

            service_ports (List[Any]): ServicePorts is the list of additional named ports to be added to the
              Services created by the operator.

            sidecar_containers (List[Any]): SidecarContainers to be used in the Pod.

            storage (Dict[str, Any]): Storage defines the storage options to be used for provisioning the
              PVCs mounted by MariaDB.

            suspend (bool): Suspend indicates whether the current resource should be suspended or
              not. This can be useful for maintenance, as disabling the
              reconciliation prevents the operator from interfering with user
              operations during maintenance activities.

            time_zone (str): TimeZone sets the default timezone. If not provided, it defaults to
              SYSTEM and the timezone data is not loaded.

            tolerations (List[Any]): Tolerations to be used in the Pod.

            topology_spread_constraints (List[Any]): TopologySpreadConstraints to be used in the Pod.

            update_strategy (Dict[str, Any]): UpdateStrategy defines how a MariaDB resource is updated.

            username (str): Username is the initial username to be created by the operator once
              MariaDB is ready. It has all privileges on the initial database.
              The initial User will have ALL PRIVILEGES in the initial Database.

            volume_mounts (List[Any]): VolumeMounts to be used in the Container.

            volumes (List[Any]): Volumes to be used in the Pod.

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
        self.password_hash_secret_key_ref = password_hash_secret_key_ref
        self.password_plugin = password_plugin
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
        self.replicas_allow_even_number = replicas_allow_even_number
        self.replication = replication
        self.resources = resources
        self.root_empty_password = root_empty_password
        self.root_password_secret_key_ref = root_password_secret_key_ref
        self.secondary_connection = secondary_connection
        self.secondary_service = secondary_service
        self.security_context = security_context
        self.service = service
        self.service_account_name = service_account_name
        self.service_ports = service_ports
        self.sidecar_containers = sidecar_containers
        self.storage = storage
        self.suspend = suspend
        self.time_zone = time_zone
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

            if self.password_hash_secret_key_ref:
                _spec["passwordHashSecretKeyRef"] = self.password_hash_secret_key_ref

            if self.password_plugin:
                _spec["passwordPlugin"] = self.password_plugin

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

            if self.replicas_allow_even_number is not None:
                _spec["replicasAllowEvenNumber"] = self.replicas_allow_even_number

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

            if self.service_ports:
                _spec["servicePorts"] = self.service_ports

            if self.sidecar_containers:
                _spec["sidecarContainers"] = self.sidecar_containers

            if self.storage:
                _spec["storage"] = self.storage

            if self.suspend is not None:
                _spec["suspend"] = self.suspend

            if self.time_zone:
                _spec["timeZone"] = self.time_zone

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

    # End of generated code
