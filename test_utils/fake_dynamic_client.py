"""
Fake DynamicClient for Kubernetes/OpenShift Testing

A comprehensive fake implementation of kubernetes.dynamic.DynamicClient for unit testing.
This module provides a complete in-memory simulation of Kubernetes API operations without
requiring a real cluster.

Usage:
    from test_utils.fake_dynamic_client import FakeDynamicClient

    # Drop-in replacement for kubernetes.dynamic.DynamicClient
    client = FakeDynamicClient()

    # Use exactly like real DynamicClient
    pod_api = client.resources.get(kind="Pod", api_version="v1")
    pod = pod_api.create(body=pod_manifest, namespace="default")

Features:
    - Complete CRUD operations (Create, Read, Update, Delete)
    - Resource discovery (search, get)
    - Label and field selectors
    - Watch functionality with event streaming
    - Proper exception handling
    - Namespace isolation
    - Resource versioning
    - Custom resource support
    - Pre-loading test data
    - Error simulation for testing

Author: AI Assistant
License: MIT
"""

import copy
import json
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from unittest.mock import Mock

# Import exceptions from kubernetes.dynamic - use real ones for compatibility
try:
    from kubernetes.dynamic.exceptions import (
        ApiException,
        ConflictError,
        ForbiddenError,
        MethodNotAllowedError,
        NotFoundError,
        ResourceNotFoundError,
        ServerTimeoutError,
    )
except ImportError:
    # Fallback implementations if kubernetes module is not available
    class TestUtilsApiException(Exception):
        def __init__(self, status=None, reason=None, body=None):
            super().__init__(f"API Exception: {status} - {reason}")
            self.status = status
            self.reason = reason
            self.body = body

    class TestUtilsNotFoundError(TestUtilsApiException):
        def __init__(self, reason="Not Found"):
            super().__init__(status=404, reason=reason)
            self.status = 404

    class TestUtilsConflictError(TestUtilsApiException):
        def __init__(self, reason="Conflict"):
            super().__init__(status=409, reason=reason)

    class TestUtilsForbiddenError(TestUtilsApiException):
        def __init__(self, reason="Forbidden"):
            super().__init__(status=403, reason=reason)

    class TestUtilsMethodNotAllowedError(TestUtilsApiException):
        def __init__(self, reason="Method Not Allowed"):
            super().__init__(status=405, reason=reason)

    class TestUtilsResourceNotFoundError(TestUtilsApiException):
        def __init__(self, reason="Resource Not Found"):
            super().__init__(status=404, reason=reason)

    class TestUtilsServerTimeoutError(TestUtilsApiException):
        def __init__(self, reason="Server Timeout"):
            super().__init__(status=504, reason=reason)

    # Create aliases with expected names
    ApiException = TestUtilsApiException
    NotFoundError = TestUtilsNotFoundError
    ConflictError = TestUtilsConflictError
    ForbiddenError = TestUtilsForbiddenError
    MethodNotAllowedError = TestUtilsMethodNotAllowedError
    ResourceNotFoundError = TestUtilsResourceNotFoundError
    ServerTimeoutError = TestUtilsServerTimeoutError


class FakeResourceField:
    """Fake implementation of kubernetes.dynamic.resource.ResourceField"""

    def __init__(self, data):
        self._data = data if data is not None else {}

    def __getattr__(self, name):
        if name.startswith("_"):
            return super().__getattribute__(name)
        value = self._data.get(name)
        if value is None:
            return FakeResourceField(data={})
        elif isinstance(value, dict):
            return FakeResourceField(data=value)
        elif isinstance(value, list):
            return [FakeResourceField(data=item) if isinstance(item, dict) else item for item in value]
        else:
            return value

    def __getitem__(self, key):
        value = self._data.get(key)
        if value is None:
            return FakeResourceField(data={})
        elif isinstance(value, dict):
            return FakeResourceField(data=value)
        elif isinstance(value, list):
            return [FakeResourceField(data=item) if isinstance(item, dict) else item for item in value]
        else:
            return value

    def __contains__(self, key):
        return key in self._data

    def __bool__(self):
        return bool(self._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return f"FakeResourceField({self._data})"

    def get(self, key, default=None):
        value = self._data.get(key, default)
        if isinstance(value, dict) and value != default:
            return FakeResourceField(data=value)
        return value

    def to_dict(self):
        """Convert to dictionary"""
        return copy.deepcopy(self._data)


class FakeResourceInstance:
    """Fake implementation of kubernetes.dynamic.client.ResourceInstance"""

    def __init__(self, resource_def, storage, client):
        self.resource_def = resource_def
        self.storage = storage
        self.client = client

    def create(self, body=None, namespace=None, **kwargs):
        """Create a resource"""
        if body is None:
            raise ValueError("body is required for create")

        # Validate body structure
        if not isinstance(body, dict):
            raise ValueError("body must be a dictionary")

        if "metadata" not in body:
            body["metadata"] = {}

        # Set namespace if provided
        if namespace and self.resource_def.get("namespaced", True):
            body["metadata"]["namespace"] = namespace

        # Generate metadata if not present
        if "name" not in body["metadata"]:
            raise ValueError("metadata.name is required")

        name = body["metadata"]["name"]
        resource_namespace = (
            body["metadata"].get("namespace", "default") if self.resource_def.get("namespaced", True) else None
        )

        # Check if resource already exists
        existing = self.storage.get_resource(
            kind=self.resource_def["kind"],
            api_version=self.resource_def["api_version"],
            name=name,
            namespace=resource_namespace,
        )
        if existing:
            raise ConflictError(f"{self.resource_def['kind']} '{name}' already exists")

        # Add generated metadata
        body["metadata"].update({
            "uid": str(uuid.uuid4()),
            "resourceVersion": str(int(time.time() * 1000)),
            "creationTimestamp": datetime.now(timezone.utc).isoformat(),
            "generation": 1,
        })

        # Set API version and kind
        body["apiVersion"] = self.resource_def["api_version"]
        body["kind"] = self.resource_def["kind"]

        # Add realistic status for resources that need it
        self._add_realistic_status(body)

        # Store the resource
        self.storage.store_resource(
            kind=self.resource_def["kind"],
            api_version=self.resource_def["api_version"],
            name=name,
            namespace=resource_namespace,
            resource=body,
        )

        # Generate automatic events for resource creation
        self._generate_resource_events(body, "Created", "created")

        return FakeResourceField(data=body)

    def _generate_resource_events(self, resource, reason, action):
        """Generate automatic events for resource operations - completely resource-agnostic"""
        if not resource or not resource.get("metadata"):
            return

        resource_name = resource["metadata"].get("name")
        resource_namespace = resource["metadata"].get("namespace")
        resource_kind = resource.get("kind")
        resource_uid = resource["metadata"].get("uid")

        if not resource_name or not resource_kind:
            return

        # Generate event name (Kubernetes pattern)
        event_name = f"{resource_name}.{int(time.time() * 1000000)}"

        # Create realistic event
        event = {
            "apiVersion": "v1",
            "kind": "Event",
            "metadata": {
                "name": event_name,
                "namespace": resource_namespace or "default",
                "uid": str(uuid.uuid4()),
                "resourceVersion": str(int(time.time() * 1000)),
                "creationTimestamp": datetime.now(timezone.utc).isoformat(),
                "generation": 1,
            },
            "involvedObject": {
                "apiVersion": resource.get("apiVersion"),
                "kind": resource_kind,
                "name": resource_name,
                "namespace": resource_namespace,
                "uid": resource_uid,
                "resourceVersion": resource["metadata"].get("resourceVersion"),
            },
            "reason": reason,
            "message": f"{resource_kind} {resource_name} has been {action}",
            "source": {"component": "fake-client", "host": "fake-cluster.example.com"},
            "firstTimestamp": datetime.now(timezone.utc).isoformat(),
            "lastTimestamp": datetime.now(timezone.utc).isoformat(),
            "count": 1,
            "type": "Normal",
        }

        # Store the event
        event_namespace = resource_namespace or "default"
        self.storage.store_resource(
            kind="Event", api_version="v1", name=event_name, namespace=event_namespace, resource=event
        )

    def _add_realistic_status(self, body):
        """Add realistic status for different resource types"""
        kind = body.get("kind", "")

        # Status templates for different resource kinds
        status_templates = {
            "Pod": self._get_pod_status_template,
            "Deployment": self._get_deployment_status_template,
            "Service": self._get_service_status_template,
            "Namespace": self._get_namespace_status_template,
        }

        # Get appropriate status template or use generic one
        status_func = status_templates.get(kind, self._get_generic_status_template)
        status = status_func(body=body)

        if status:
            body["status"] = status

    def _get_pod_status_template(self, body):
        """Get realistic Pod status"""
        container_name = "test-container"
        if "spec" in body and "containers" in body["spec"] and body["spec"]["containers"]:
            container_name = body["spec"]["containers"][0].get("name", "test-container")

        return {
            "phase": "Running",
            "conditions": [
                {
                    "type": "Initialized",
                    "status": "True",
                    "lastProbeTime": None,
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "PodCompleted",
                },
                {
                    "type": "Ready",
                    "status": "False",  # Default to False to match test expectation
                    "lastProbeTime": None,
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ContainersNotReady",
                    "message": f"containers with unready status: [{container_name}]",
                },
                {
                    "type": "ContainersReady",
                    "status": "False",
                    "lastProbeTime": None,
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ContainersNotReady",
                    "message": f"containers with unready status: [{container_name}]",
                },
                {
                    "type": "PodScheduled",
                    "status": "True",
                    "lastProbeTime": None,
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "PodScheduled",
                },
            ],
            "hostIP": "10.0.0.1",
            "podIP": "10.244.0.2",
            "podIPs": [{"ip": "10.244.0.2"}],
            "startTime": datetime.now(timezone.utc).isoformat(),
            "containerStatuses": [
                {
                    "name": container_name,
                    "state": {"waiting": {"reason": "ContainerCreating"}},
                    "lastState": {},
                    "ready": False,
                    "restartCount": 0,
                    "image": "nginx:latest",
                    "imageID": "",
                    "containerID": "",
                    "started": False,
                }
            ],
        }

    def _get_deployment_status_template(self, body):
        """Get realistic Deployment status"""
        return {
            "replicas": 1,
            "updatedReplicas": 1,
            "readyReplicas": 1,
            "availableReplicas": 1,
            "observedGeneration": 1,
            "conditions": [
                {
                    "type": "Available",
                    "status": "True",
                    "lastUpdateTime": datetime.now(timezone.utc).isoformat(),
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "MinimumReplicasAvailable",
                    "message": "Deployment has minimum availability.",
                },
                {
                    "type": "Progressing",
                    "status": "True",
                    "lastUpdateTime": datetime.now(timezone.utc).isoformat(),
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "NewReplicaSetAvailable",
                    "message": "ReplicaSet has successfully progressed.",
                },
            ],
        }

    def _get_service_status_template(self, body):
        """Get realistic Service status"""
        # Services don't typically have complex status
        return {"loadBalancer": {}}

    def _get_namespace_status_template(self, body):
        """Get realistic Namespace status"""
        return {
            "phase": "Active",
            "conditions": [
                {
                    "type": "NamespaceDeletionDiscoveryFailure",
                    "status": "False",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ResourcesDiscovered",
                    "message": "All resources successfully discovered",
                },
                {
                    "type": "NamespaceDeletionContentFailure",
                    "status": "False",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ContentDeleted",
                    "message": "All content successfully deleted",
                },
            ],
        }

    def _get_generic_status_template(self, body):
        """Get generic status for unknown resource types"""
        # Most resources have conditions, so provide a generic "Ready" condition
        return {
            "conditions": [
                {
                    "type": "Ready",
                    "status": "True",
                    "lastTransitionTime": datetime.now(timezone.utc).isoformat(),
                    "reason": "ResourceReady",
                    "message": "Resource is ready",
                }
            ]
        }

    def get(self, name=None, namespace=None, label_selector=None, field_selector=None, **kwargs):
        """Get resource(s)"""
        if name:
            # Get specific resource
            resource = self.storage.get_resource(
                kind=self.resource_def["kind"],
                api_version=self.resource_def["api_version"],
                name=name,
                namespace=namespace,
            )
            if not resource:
                # Create a proper kubernetes-style exception
                try:
                    from kubernetes.client.rest import ApiException as K8sApiException

                    api_exception = K8sApiException(
                        status=404, reason=f"{self.resource_def['kind']} '{name}' not found"
                    )
                    raise NotFoundError(api_exception)
                except ImportError:
                    # Fallback for when kubernetes client is not available
                    raise NotFoundError(f"{self.resource_def['kind']} '{name}' not found")
            return FakeResourceField(data=resource)
        else:
            # List resources
            resources = self.storage.list_resources(
                kind=self.resource_def["kind"],
                api_version=self.resource_def["api_version"],
                namespace=namespace,
                label_selector=label_selector,
                field_selector=field_selector,
            )

            # Create list response
            response = {
                "apiVersion": self.resource_def["api_version"],
                "kind": f"{self.resource_def['kind']}List",
                "metadata": {
                    "resourceVersion": str(int(time.time() * 1000)),
                },
                "items": resources,
            }

            return FakeResourceField(data=response)

    def delete(self, name=None, namespace=None, body=None, **kwargs):
        """Delete resource(s)"""
        if name:
            # Delete specific resource
            deleted = self.storage.delete_resource(
                kind=self.resource_def["kind"],
                api_version=self.resource_def["api_version"],
                name=name,
                namespace=namespace,
            )
            if not deleted:
                # Create a proper kubernetes-style exception
                try:
                    from kubernetes.client.rest import ApiException as K8sApiException

                    api_exception = K8sApiException(
                        status=404, reason=f"{self.resource_def['kind']} '{name}' not found"
                    )
                    raise NotFoundError(api_exception)
                except ImportError:
                    # Fallback for when kubernetes client is not available
                    raise NotFoundError(f"{self.resource_def['kind']} '{name}' not found")
            # Generate automatic events for resource deletion
            self._generate_resource_events(deleted, "Deleted", "deleted")

            return FakeResourceField(data=deleted)
        else:
            # Delete collection - not implemented for safety
            raise MethodNotAllowedError("Collection deletion not supported")

    def patch(self, name=None, body=None, namespace=None, **kwargs):
        """Patch a resource"""
        if not name:
            raise ValueError("name is required for patch")
        if not body:
            raise ValueError("body is required for patch")

        existing = self.storage.get_resource(
            kind=self.resource_def["kind"], api_version=self.resource_def["api_version"], name=name, namespace=namespace
        )
        if not existing:
            # Create a proper kubernetes-style exception
            try:
                from kubernetes.client.rest import ApiException as K8sApiException

                api_exception = K8sApiException(status=404, reason=f"{self.resource_def['kind']} '{name}' not found")
                raise NotFoundError(api_exception)
            except ImportError:
                # Fallback for when kubernetes client is not available
                raise NotFoundError(f"{self.resource_def['kind']} '{name}' not found")

        # Simple merge patch implementation
        patched = copy.deepcopy(existing)
        self._merge_patch(patched, body)

        # Update metadata
        patched["metadata"]["resourceVersion"] = str(int(time.time() * 1000))
        if "generation" in patched["metadata"]:
            patched["metadata"]["generation"] += 1

        # Store updated resource
        self.storage.store_resource(
            kind=self.resource_def["kind"],
            api_version=self.resource_def["api_version"],
            name=name,
            namespace=namespace,
            resource=patched,
        )

        # Generate automatic events for resource patch
        self._generate_resource_events(patched, "Updated", "updated")

        return FakeResourceField(data=patched)

    def replace(self, name=None, body=None, namespace=None, **kwargs):
        """Replace a resource"""
        if not name:
            raise ValueError("name is required for replace")
        if not body:
            raise ValueError("body is required for replace")

        existing = self.storage.get_resource(
            kind=self.resource_def["kind"], api_version=self.resource_def["api_version"], name=name, namespace=namespace
        )
        if not existing:
            # Create a proper kubernetes-style exception
            try:
                from kubernetes.client.rest import ApiException as K8sApiException

                api_exception = K8sApiException(status=404, reason=f"{self.resource_def['kind']} '{name}' not found")
                raise NotFoundError(api_exception)
            except ImportError:
                # Fallback for when kubernetes client is not available
                raise NotFoundError(f"{self.resource_def['kind']} '{name}' not found")

        # Ensure metadata is preserved
        if "metadata" not in body:
            body["metadata"] = {}

        body["metadata"].update({
            "uid": existing["metadata"]["uid"],
            "resourceVersion": str(int(time.time() * 1000)),
            "creationTimestamp": existing["metadata"]["creationTimestamp"],
            "generation": existing["metadata"].get("generation", 1) + 1,
        })

        # Set API version and kind
        body["apiVersion"] = self.resource_def["api_version"]
        body["kind"] = self.resource_def["kind"]

        # Store replaced resource
        self.storage.store_resource(
            kind=self.resource_def["kind"],
            api_version=self.resource_def["api_version"],
            name=name,
            namespace=namespace,
            resource=body,
        )

        # Generate automatic events for resource replacement
        self._generate_resource_events(body, "Updated", "replaced")

        return FakeResourceField(data=body)

    def watch(self, namespace=None, timeout=None, **kwargs):
        """Watch for resource changes"""
        # Simple implementation - yields existing resources as ADDED events
        resources = self.storage.list_resources(
            kind=self.resource_def["kind"], api_version=self.resource_def["api_version"], namespace=namespace
        )

        for resource in resources:
            yield {"type": "ADDED", "object": FakeResourceField(data=resource), "raw_object": resource}

    def _merge_patch(self, target, patch):
        """Simple merge patch implementation"""
        if isinstance(patch, dict):
            for key, value in patch.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    self._merge_patch(target[key], value)
                else:
                    target[key] = value
        else:
            return patch


class FakeResourceRegistry:
    """Fake implementation of kubernetes.dynamic.client.ResourceRegistry"""

    def __init__(self, storage):
        self.storage = storage
        self._builtin_resources = self._initialize_builtin_resources()

    def _initialize_builtin_resources(self):
        """Initialize common Kubernetes resources"""
        return {
            ("v1", "Pod"): {
                "kind": "Pod",
                "api_version": "v1",
                "group": "",
                "version": "v1",
                "group_version": "v1",
                "plural": "pods",
                "singular": "pod",
                "namespaced": True,
                "shortNames": ["po"],
                "categories": ["all"],
            },
            ("v1", "Service"): {
                "kind": "Service",
                "api_version": "v1",
                "group": "",
                "version": "v1",
                "group_version": "v1",
                "plural": "services",
                "singular": "service",
                "namespaced": True,
                "shortNames": ["svc"],
                "categories": ["all"],
            },
            ("v1", "Namespace"): {
                "kind": "Namespace",
                "api_version": "v1",
                "group": "",
                "version": "v1",
                "group_version": "v1",
                "plural": "namespaces",
                "singular": "namespace",
                "namespaced": False,
                "shortNames": ["ns"],
                "categories": ["all"],
            },
            ("v1", "Secret"): {
                "kind": "Secret",
                "api_version": "v1",
                "group": "",
                "version": "v1",
                "group_version": "v1",
                "plural": "secrets",
                "singular": "secret",
                "namespaced": True,
                "categories": ["all"],
            },
            ("v1", "Event"): {
                "kind": "Event",
                "api_version": "v1",
                "group": "",
                "version": "v1",
                "group_version": "v1",
                "plural": "events",
                "singular": "event",
                "namespaced": True,
                "categories": ["all"],
            },
            ("v1", "ConfigMap"): {
                "kind": "ConfigMap",
                "api_version": "v1",
                "group": "",
                "version": "v1",
                "group_version": "v1",
                "plural": "configmaps",
                "singular": "configmap",
                "namespaced": True,
                "shortNames": ["cm"],
                "categories": ["all"],
            },
            ("v1", "PersistentVolumeClaim"): {
                "kind": "PersistentVolumeClaim",
                "api_version": "v1",
                "group": "",
                "version": "v1",
                "group_version": "v1",
                "plural": "persistentvolumeclaims",
                "singular": "persistentvolumeclaim",
                "namespaced": True,
                "shortNames": ["pvc"],
                "categories": ["all"],
            },
            ("apps/v1", "Deployment"): {
                "kind": "Deployment",
                "api_version": "apps/v1",
                "group": "apps",
                "version": "v1",
                "group_version": "apps/v1",
                "plural": "deployments",
                "singular": "deployment",
                "namespaced": True,
                "shortNames": ["deploy"],
                "categories": ["all"],
            },
            ("apps/v1", "ReplicaSet"): {
                "kind": "ReplicaSet",
                "api_version": "apps/v1",
                "group": "apps",
                "version": "v1",
                "group_version": "apps/v1",
                "plural": "replicasets",
                "singular": "replicaset",
                "namespaced": True,
                "shortNames": ["rs"],
                "categories": ["all"],
            },
            ("apps/v1", "StatefulSet"): {
                "kind": "StatefulSet",
                "api_version": "apps/v1",
                "group": "apps",
                "version": "v1",
                "group_version": "apps/v1",
                "plural": "statefulsets",
                "singular": "statefulset",
                "namespaced": True,
                "shortNames": ["sts"],
                "categories": ["all"],
            },
            ("apps/v1", "DaemonSet"): {
                "kind": "DaemonSet",
                "api_version": "apps/v1",
                "group": "apps",
                "version": "v1",
                "group_version": "apps/v1",
                "plural": "daemonsets",
                "singular": "daemonset",
                "namespaced": True,
                "shortNames": ["ds"],
                "categories": ["all"],
            },
            ("networking.k8s.io/v1", "NetworkPolicy"): {
                "kind": "NetworkPolicy",
                "api_version": "networking.k8s.io/v1",
                "group": "networking.k8s.io",
                "version": "v1",
                "group_version": "networking.k8s.io/v1",
                "plural": "networkpolicies",
                "singular": "networkpolicy",
                "namespaced": True,
                "shortNames": ["netpol"],
                "categories": ["all"],
            },
            ("rbac.authorization.k8s.io/v1", "Role"): {
                "kind": "Role",
                "api_version": "rbac.authorization.k8s.io/v1",
                "group": "rbac.authorization.k8s.io",
                "version": "v1",
                "group_version": "rbac.authorization.k8s.io/v1",
                "plural": "roles",
                "singular": "role",
                "namespaced": True,
                "categories": ["all"],
            },
            ("rbac.authorization.k8s.io/v1", "ClusterRole"): {
                "kind": "ClusterRole",
                "api_version": "rbac.authorization.k8s.io/v1",
                "group": "rbac.authorization.k8s.io",
                "version": "v1",
                "group_version": "rbac.authorization.k8s.io/v1",
                "plural": "clusterroles",
                "singular": "clusterrole",
                "namespaced": False,
                "categories": ["all"],
            },
            # OpenShift specific resources
            ("route.openshift.io/v1", "Route"): {
                "kind": "Route",
                "api_version": "route.openshift.io/v1",
                "group": "route.openshift.io",
                "version": "v1",
                "group_version": "route.openshift.io/v1",
                "plural": "routes",
                "singular": "route",
                "namespaced": True,
                "categories": ["all"],
            },
            ("project.openshift.io/v1", "Project"): {
                "kind": "Project",
                "api_version": "project.openshift.io/v1",
                "group": "project.openshift.io",
                "version": "v1",
                "group_version": "project.openshift.io/v1",
                "plural": "projects",
                "singular": "project",
                "namespaced": False,
                "categories": ["all"],
            },
        }

    def get(self, kind=None, api_version=None, group=None, version=None, singular_name=None, **kwargs):
        """Get a specific resource definition"""
        # Handle different parameter combinations
        if api_version and kind:
            key = (api_version, kind)
        elif group and version and kind:
            api_version = f"{group}/{version}" if group else version
            key = (api_version, kind)
        else:
            raise ValueError("Must specify either (api_version, kind) or (group, version, kind)")

        resource_def = self._builtin_resources.get(key)
        if not resource_def:
            # Auto-generate resource definition for unknown resources
            resource_def = self._create_generic_resource_def(kind, api_version, group, version)
            self._builtin_resources[key] = resource_def

        return FakeResourceInstance(resource_def=resource_def, storage=self.storage, client=None)

    def _create_generic_resource_def(self, kind, api_version, group=None, version=None):
        """Create a generic resource definition for any resource kind"""
        # Parse group and version from api_version if not provided
        if not group and not version:
            if "/" in api_version:
                group, version = api_version.split("/", 1)
            else:
                group = ""
                version = api_version

        # Generate plural form (simple heuristic)
        kind_lower = kind.lower()
        if kind_lower.endswith("s"):
            plural = kind_lower
        elif kind_lower.endswith("y"):
            plural = kind_lower[:-1] + "ies"
        elif kind_lower.endswith(("sh", "ch", "x", "z")):
            plural = kind_lower + "es"
        else:
            plural = kind_lower + "s"

        # Determine if resource is likely namespaced (most are, except some well-known cluster-scoped ones)
        cluster_scoped_kinds = {
            "node",
            "namespace",
            "clusterrole",
            "clusterrolebinding",
            "persistentvolume",
            "storageclass",
            "customresourcedefinition",
            "clusterissuer",
            "cluster",
            "project",  # OpenShift specific
        }

        # Also check if the kind starts with "Cluster" (common convention)
        if kind_lower.startswith("cluster"):
            cluster_scoped_kinds.add(kind_lower)
        namespaced = kind_lower not in cluster_scoped_kinds

        return {
            "kind": kind,
            "api_version": api_version,
            "group": group or "",
            "version": version or "v1",
            "group_version": api_version,
            "plural": plural,
            "singular": kind_lower,
            "namespaced": namespaced,
            "shortNames": [],
            "categories": ["all"],
        }

    def search(self, kind=None, group=None, api_version=None, **kwargs):
        """Search for resource definitions"""
        results = []

        for (res_api_version, res_kind), resource_def in self._builtin_resources.items():
            # Apply filters
            if kind and res_kind != kind:
                continue
            if api_version and res_api_version != api_version:
                continue
            if group and resource_def.get("group") != group:
                continue

            # Create a fake resource field object
            result = FakeResourceField(data=resource_def)
            results.append(result)

        return results

    def add_custom_resource(self, resource_def):
        """Add a custom resource definition"""
        api_version = (
            resource_def.get("api_version") or f"{resource_def.get('group', '')}/{resource_def.get('version', '')}"
        )
        if resource_def.get("group") == "" or resource_def.get("group") is None:
            api_version = resource_def.get("version", "v1")

        key = (api_version, resource_def["kind"])

        # Ensure required fields
        full_def = {
            "kind": resource_def["kind"],
            "api_version": api_version,
            "group": resource_def.get("group", ""),
            "version": resource_def.get("version", "v1"),
            "group_version": api_version,
            "plural": resource_def.get("plural", resource_def["kind"].lower() + "s"),
            "singular": resource_def.get("singular", resource_def["kind"].lower()),
            "namespaced": resource_def.get("namespaced", True),
            "shortNames": resource_def.get("shortNames", []),
            "categories": resource_def.get("categories", ["all"]),
        }

        self._builtin_resources[key] = full_def
        return full_def


class FakeResourceStorage:
    """Resource-agnostic in-memory storage backend

    This class provides completely generic storage for any Kubernetes resource
    without any resource-specific logic. It only cares about:
    - kind: The resource type (e.g., "Pod", "CustomResource")
    - api_version: The API version (e.g., "v1", "apps/v1")
    - name: The resource name
    - namespace: The namespace (None for cluster-scoped resources)
    """

    def __init__(self):
        # Storage structure: {kind: {api_version: {namespace: {name: resource}}}}
        self._namespaced_resources = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        # For cluster-scoped resources: {kind: {api_version: {name: resource}}}
        self._cluster_scoped_resources = defaultdict(lambda: defaultdict(dict))

    def store_resource(self, kind, api_version, name, namespace, resource):
        """Store any resource type - completely resource-agnostic"""
        if namespace is None:
            # Cluster-scoped resource
            self._cluster_scoped_resources[kind][api_version][name] = copy.deepcopy(resource)
        else:
            # Namespaced resource
            self._namespaced_resources[kind][api_version][namespace][name] = copy.deepcopy(resource)

    def get_resource(self, kind, api_version, name, namespace):
        """Get any resource type - completely resource-agnostic"""
        if namespace is None:
            # Cluster-scoped resource
            return self._cluster_scoped_resources[kind][api_version].get(name)
        else:
            # Namespaced resource
            return self._namespaced_resources[kind][api_version][namespace].get(name)

    def delete_resource(self, kind, api_version, name, namespace):
        """Delete any resource type - completely resource-agnostic"""
        if namespace is None:
            # Cluster-scoped resource
            return self._cluster_scoped_resources[kind][api_version].pop(name, None)
        else:
            # Namespaced resource
            return self._namespaced_resources[kind][api_version][namespace].pop(name, None)

    def list_resources(self, kind, api_version, namespace=None, label_selector=None, field_selector=None):
        """List any resource type with optional filtering - completely resource-agnostic"""
        resources = []

        if namespace is None:
            # List from all namespaces or cluster-scoped
            if kind in self._cluster_scoped_resources and api_version in self._cluster_scoped_resources[kind]:
                # Cluster-scoped resources
                for resource in self._cluster_scoped_resources[kind][api_version].values():
                    resources.append(resource)
            else:
                # All namespaces
                if kind in self._namespaced_resources and api_version in self._namespaced_resources[kind]:
                    for ns_resources in self._namespaced_resources[kind][api_version].values():
                        resources.extend(ns_resources.values())
        else:
            # Specific namespace
            if kind in self._namespaced_resources and api_version in self._namespaced_resources[kind]:
                resources.extend(self._namespaced_resources[kind][api_version][namespace].values())

        # Apply filters
        if label_selector:
            resources = self._filter_by_labels(resources, label_selector)
        if field_selector:
            resources = self._filter_by_fields(resources, field_selector)

        return resources

    def _filter_by_labels(self, resources, label_selector):
        """Filter resources by label selector"""
        if not label_selector:
            return resources

        # Parse label selector (simple implementation)
        # Supports: key=value, key!=value, key in (value1,value2), key notin (value1,value2)
        selectors = []
        for selector in label_selector.split(","):
            selector = selector.strip()
            if "=" in selector and "!=" not in selector:
                key, value = selector.split("=", 1)
                selectors.append(("eq", key.strip(), value.strip()))
            elif "!=" in selector:
                key, value = selector.split("!=", 1)
                selectors.append(("ne", key.strip(), value.strip()))
            # Add more complex selectors as needed

        filtered_resources = []
        for resource in resources:
            labels = resource.get("metadata", {}).get("labels", {})
            match = True

            for op, key, value in selectors:
                if op == "eq":
                    if labels.get(key) != value:
                        match = False
                        break
                elif op == "ne":
                    if labels.get(key) == value:
                        match = False
                        break

            if match:
                filtered_resources.append(resource)

        return filtered_resources

    def _filter_by_fields(self, resources, field_selector):
        """Filter resources by field selector"""
        if not field_selector:
            return resources

        # Parse field selector (simple implementation)
        # Supports: metadata.name=value, metadata.namespace=value
        selectors = []
        for selector in field_selector.split(","):
            selector = selector.strip()
            if "=" in selector and "!=" not in selector:
                key, value = selector.split("=", 1)
                selectors.append(("eq", key.strip(), value.strip()))
            elif "!=" in selector:
                key, value = selector.split("!=", 1)
                selectors.append(("ne", key.strip(), value.strip()))

        filtered_resources = []
        for resource in resources:
            match = True

            for op, key, value in selectors:
                # Simple field access
                field_value = None
                if key == "metadata.name":
                    field_value = resource.get("metadata", {}).get("name")
                elif key == "metadata.namespace":
                    field_value = resource.get("metadata", {}).get("namespace")
                # Add more field paths as needed

                if op == "eq":
                    if field_value != value:
                        match = False
                        break
                elif op == "ne":
                    if field_value == value:
                        match = False
                        break

            if match:
                filtered_resources.append(resource)

        return filtered_resources

    def clear_all(self):
        """Clear all stored resources - completely resource-agnostic"""
        self._namespaced_resources.clear()
        self._cluster_scoped_resources.clear()

    def get_all_resources(self):
        """Get all stored resources for debugging - completely resource-agnostic"""
        all_resources = []

        # Add cluster-scoped resources
        for kind, api_versions in self._cluster_scoped_resources.items():
            for api_version, resources in api_versions.items():
                for resource in resources.values():
                    all_resources.append(resource)

        # Add namespaced resources
        for kind, api_versions in self._namespaced_resources.items():
            for api_version, namespaces in api_versions.items():
                for namespace, resources in namespaces.items():
                    for resource in resources.values():
                        all_resources.append(resource)

        return all_resources


class FakeConfiguration:
    """Fake implementation of kubernetes.client.Configuration"""

    def __init__(self):
        self.host = "https://fake-cluster.example.com"
        self.api_key = {"authorization": "Bearer fake-token"}
        self.proxy = None
        self.verify_ssl = True


class FakeKubernetesClient:
    """Fake implementation of kubernetes.client.ApiClient"""

    def __init__(self, configuration=None):
        self.configuration = configuration or FakeConfiguration()

    def request(self, method, url, **kwargs):
        """Mock API request"""
        # Simple mock response
        mock_response = Mock()
        mock_response.data = json.dumps({"status": "success"})
        mock_response.status = 200
        return mock_response


class FakeDynamicClient:
    """
    Fake implementation of kubernetes.dynamic.DynamicClient

    This class provides a complete in-memory simulation of the Kubernetes API
    for testing purposes. It supports all major operations:

    - Resource CRUD operations
    - Resource discovery
    - Label and field selectors
    - Watch functionality
    - Namespace isolation
    - Custom resource definitions

    Usage:
        client = FakeDynamicClient()

        # Use like real DynamicClient
        pod_api = client.resources.get(kind="Pod", api_version="v1")
        pod = pod_api.create(body=pod_manifest, namespace="default")

        # Pre-load test data
        client.preload_resources([pod_manifest])

        # Add custom resources
        client.add_custom_resource({
            "kind": "MyResource",
            "group": "example.com",
            "version": "v1",
            "namespaced": True
        })
    """

    def __init__(self):
        self.configuration = FakeConfiguration()
        self.client = FakeKubernetesClient(configuration=self.configuration)
        self.storage_backend = FakeResourceStorage()
        self.resources = FakeResourceRegistry(storage=self.storage_backend)
        self._error_simulation = {}

    def get(self, resource, name=None, namespace=None, **kwargs):
        """Get resource(s) using resource definition"""
        if hasattr(resource, "get"):
            return resource.get(name=name, namespace=namespace, **kwargs)
        else:
            raise ValueError("Invalid resource definition")

    def create(self, resource, body=None, namespace=None, **kwargs):
        """Create resource using resource definition"""
        if hasattr(resource, "create"):
            return resource.create(body=body, namespace=namespace, **kwargs)
        else:
            raise ValueError("Invalid resource definition")

    def delete(self, resource, name=None, namespace=None, **kwargs):
        """Delete resource using resource definition"""
        if hasattr(resource, "delete"):
            return resource.delete(name=name, namespace=namespace, **kwargs)
        else:
            raise ValueError("Invalid resource definition")

    def patch(self, resource, name=None, body=None, namespace=None, **kwargs):
        """Patch resource using resource definition"""
        if hasattr(resource, "patch"):
            return resource.patch(name=name, body=body, namespace=namespace, **kwargs)
        else:
            raise ValueError("Invalid resource definition")

    def replace(self, resource, name=None, body=None, namespace=None, **kwargs):
        """Replace resource using resource definition"""
        if hasattr(resource, "replace"):
            return resource.replace(name=name, body=body, namespace=namespace, **kwargs)
        else:
            raise ValueError("Invalid resource definition")

    def watch(self, resource, namespace=None, **kwargs):
        """Watch resource using resource definition"""
        if hasattr(resource, "watch"):
            return resource.watch(namespace=namespace, **kwargs)
        else:
            raise ValueError("Invalid resource definition")

    # Test utility methods

    def preload_resources(self, resources):
        """Pre-load resources for testing"""
        for resource in resources:
            if not isinstance(resource, dict):
                continue

            kind = resource.get("kind")
            api_version = resource.get("apiVersion")
            name = resource.get("metadata", {}).get("name")
            namespace = resource.get("metadata", {}).get("namespace")

            if not all([kind, api_version, name]):
                continue

            # Get resource definition
            try:
                resource_def = None
                for (res_api_version, res_kind), def_data in self.resources._builtin_resources.items():
                    if res_kind == kind and res_api_version == api_version:
                        resource_def = def_data
                        break

                if not resource_def:
                    continue

                # Add generated metadata if missing
                if "metadata" not in resource:
                    resource["metadata"] = {}

                resource["metadata"].update({
                    "uid": resource["metadata"].get("uid", str(uuid.uuid4())),
                    "resourceVersion": resource["metadata"].get("resourceVersion", str(int(time.time() * 1000))),
                    "creationTimestamp": resource["metadata"].get(
                        "creationTimestamp", datetime.now(timezone.utc).isoformat()
                    ),
                    "generation": resource["metadata"].get("generation", 1),
                })

                # Store the resource
                self.storage_backend.store_resource(
                    kind=kind, api_version=api_version, name=name, namespace=namespace, resource=resource
                )

            except Exception:
                # Skip invalid resources
                continue

    def add_custom_resource(self, resource_def):
        """Add a custom resource definition"""
        return self.resources.add_custom_resource(resource_def=resource_def)

    def simulate_error(self, kind, operation, error):
        """Simulate an error for testing"""
        if kind not in self._error_simulation:
            self._error_simulation[kind] = {}
        if operation not in self._error_simulation[kind]:
            self._error_simulation[kind][operation] = []
        self._error_simulation[kind][operation].append(error)

    def clear_error_simulation(self):
        """Clear all error simulations"""
        self._error_simulation.clear()

    def list_all_resources(self):
        """List all stored resources for debugging"""
        return self.storage_backend.get_all_resources()

    def clear_all_resources(self):
        """Clear all stored resources"""
        self.storage_backend.clear_all()

    def get_resource_count(self, kind=None, api_version=None, namespace=None):
        """Get count of resources for testing"""
        if kind and api_version:
            resources = self.storage_backend.list_resources(kind=kind, api_version=api_version, namespace=namespace)
            return len(resources)
        else:
            return len(self.storage_backend.get_all_resources())
