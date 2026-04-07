import warnings
from collections.abc import Generator
from datetime import datetime, timedelta, timezone
from typing import Any

from kubernetes.dynamic import DynamicClient
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class Event:
    """
    Allow read and remove K8s events.
    """

    api_version = "v1"

    # TODO: remove once `client` is mandatory
    @staticmethod
    def _resolve_client(
        client: DynamicClient | None,
        dyn_client: DynamicClient | None,
    ) -> DynamicClient:
        """Resolve client from new or deprecated parameter with deprecation warning."""
        if client is None and dyn_client is not None:
            warnings.warn(
                "`dyn_client` arg will be renamed to `client` and will be mandatory in the next major release.",
                FutureWarning,
                stacklevel=3,  # Adjusted for helper function call
            )

        resolved = client or dyn_client
        assert resolved is not None, "Either 'client' or 'dyn_client' must be provided"
        return resolved

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
        _client = cls._resolve_client(client, dyn_client)

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

    @staticmethod
    def _parse_timestamp(event: Any) -> datetime | None:
        """Parse event timestamp, preferring lastTimestamp over creationTimestamp."""
        timestamp = event.get("lastTimestamp") or event.get("metadata", {}).get("creationTimestamp")
        if not timestamp:
            return None
        try:
            return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            LOGGER.debug(f"Failed to parse event timestamp: {timestamp}")
            return None

    @classmethod
    def list(
        cls,
        client: DynamicClient,
        namespace: str | None = None,
        field_selector: str | None = None,
        label_selector: str | None = None,
        since_seconds: int = 300,
    ) -> list[Any]:
        """
        List existing K8s events using a standard API list call (not watch).

        Unlike ``Event.get()`` which uses watch and streams events in real-time,
        this method returns already-existing events immediately.

        Args:
            client: K8s dynamic client.
            namespace: Filter events to this namespace.
            field_selector: Filter events by fields (e.g. ``"type==Warning"``).
            label_selector: Filter events by labels.
            since_seconds: Only return events from the last N seconds (default: 300 = 5 minutes).

        Returns:
            List of event resource objects, sorted by ``lastTimestamp`` descending (most recent first).

        Example:
            List Warning events from the last 5 minutes in a namespace::

                events = Event.list(
                    client=client,
                    namespace="my-namespace",
                    field_selector="type==Warning",
                )
        """
        if since_seconds < 0:
            raise ValueError("since_seconds must be >= 0")

        LOGGER.info("Listing events")
        LOGGER.debug(
            f"list events parameters: namespace={namespace},"
            f" field_selector='{field_selector}', label_selector='{label_selector}',"
            f" since_seconds={since_seconds}"
        )

        resource = client.resources.get(api_version=cls.api_version, kind=cls.__name__)
        kwargs: dict[str, Any] = {}
        if namespace:
            kwargs["namespace"] = namespace
        if field_selector:
            kwargs["field_selector"] = field_selector
        if label_selector:
            kwargs["label_selector"] = label_selector

        response = resource.get(**kwargs)
        events = response.items or []

        cutoff = datetime.now(tz=timezone.utc) - timedelta(seconds=since_seconds)
        timed_events: list[tuple[datetime, Any]] = []
        for event in events:
            event_time = cls._parse_timestamp(event)
            if event_time and event_time >= cutoff:
                timed_events.append((event_time, event))

        timed_events.sort(key=lambda pair: pair[0], reverse=True)
        return [event for _, event in timed_events]

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

        example: deleting all the events with a reason of "AnEventReason", from "my-namespace" namespace
            def delete_events_before_test(client):
                Event.delete_events(client=client, namespace="my-namespace", field_selector="reason=AnEventReason")
        """
        _client = cls._resolve_client(client, dyn_client)

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
