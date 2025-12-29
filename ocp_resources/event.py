import warnings
from collections.abc import Generator
from typing import Any

from kubernetes.dynamic import DynamicClient
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class Event:
    """
    Allow read and remove K8s events.
    """

    api_version = "v1"

    @classmethod
    def get(
        cls,
        client: DynamicClient | None = None,  # TODO: make mandatory in the next major release
        dyn_client: DynamicClient | None = None,  # TODO: remove in the next major release
        namespace: str | None = None,
        name: str | None = None,
        label_selector: str | None = None,
        field_selector: str | None = None,
        resource_version: str | None = None,
        timeout: int | None = None,
    ) -> Generator[Any, None, None]:
        """
        get - retrieves K8s events.

        Args:
            client (DynamicClient): K8s client
            dyn_client (DynamicClient): K8s client
            namespace (str): event namespace
            name (str): event name
            label_selector (str): filter events by labels; comma separated string of key=value
            field_selector (str): filter events by fields; comma separated string of key=valueevent fields;
                comma separated string of key=value
            resource_version (str): filter events by their resource's version
            timeout (int): timeout in seconds

        Returns
            list: event objects

        example: reading all CSV Warning events in namespace "my-namespace", with reason of "AnEventReason"
              for event in Event.get(
                  default_client,
                  namespace="my-namespace",
                  field_selector="involvedObject.kind==ClusterServiceVersion,type==Warning,reason=AnEventReason",
                  timeout=10,
              ):
                print(event.object)
        """
        _client = client or dyn_client

        warnings.warn(
            "`dyn_client` arg will be renamed to `client` and will be mandatory in the next major release. ",
            FutureWarning,
            stacklevel=2,
        )

        assert _client is not None, "Either 'client' or 'dyn_client' must be provided"

        LOGGER.info("Reading events")
        LOGGER.debug(
            f"get events parameters: namespace={namespace}, name={name},"
            f" label_selector={label_selector}, field_selector='{field_selector}',"
            f" resource_version={resource_version}, timeout={timeout}"
        )

        event_listener = _client.resources.get(api_version=cls.api_version, kind=cls.__name__)
        yield from event_listener.watch(
            namespace=namespace,
            name=name,
            label_selector=label_selector,
            field_selector=field_selector,
            resource_version=resource_version,
            timeout=timeout,
        )

    @classmethod
    def delete_events(
        cls,
        client: DynamicClient | None = None,  # TODO: make mandatory in the next major release
        dyn_client: DynamicClient | None = None,  # TODO: remove in the next major release
        namespace: str | None = None,
        name: str | None = None,
        label_selector: str | None = None,
        field_selector: str | None = None,
        resource_version: str | None = None,
        timeout: int | None = None,
    ) -> None:
        """
        delete_events - delete K8s events. For example, to cleanup events before test, in order to not get old
            events in the test, in order to prevent false positive test.

        Args:
            client (DynamicClient): K8s client
            dyn_client (DynamicClient): K8s client
            namespace (str): event namespace
            name (str): event name
            label_selector (str): filter events by labels; comma separated string of key=value
            field_selector (str): filter events by fields; comma separated string of key=valueevent fields;
                comma separated string of key=value
            resource_version (str): filter events by their resource's version
            timeout (int): timeout in seconds

        Returns
            list: event objects

        example: deleting all the event with a reason of "AnEventReason", from "my-namespace" namespace

        def delete_events_before_test(default_client):
          Event.delete_events(default_client, namespace=my-namespace, field_selector="reason=AnEventReason")
        """
        _client = client or dyn_client

        warnings.warn(
            "`dyn_client` arg will be renamed to `client` and will be mandatory in the next major release. ",
            FutureWarning,
            stacklevel=2,
        )

        assert _client is not None, "Either 'client' or 'dyn_client' must be provided"

        LOGGER.info("Deleting events")
        LOGGER.debug(
            f"delete_events parameters: namespace={namespace}, name={name},"
            f" label_selector={label_selector}, field_selector='{field_selector}',"
            f" resource_version={resource_version}, timeout={timeout}"
        )

        _client.resources.get(api_version=cls.api_version, kind=cls.__name__).delete(
            namespace=namespace,
            name=name,
            label_selector=label_selector,
            field_selector=field_selector,
            resource_version=resource_version,
            timeout=timeout,
        )
