import logging

from ocp_resources.resource import NamespacedResource


LOGGER = logging.getLogger(__name__)


class Event(NamespacedResource):
    """
    Allow read and remove K8s events.
    """

    api_version = NamespacedResource.ApiVersion.V1

    @classmethod
    def get(
        cls,
        dyn_client,
        name=None,
        namespace=None,
        label_selector=None,
        field_selector=None,
        resource_version=None,
        timeout=None,
    ):
        """

        Args:
            dyn_client (obj): K8s client
            namespace (str, optionl): event namespace
            name (str, optionl): event name
            label_selector (str, optionl): filter events by labels; comma separated string of key=value
            field_selector (str, optional): filter events by event fields; comma separated string of key=value
            resource_version (str, optional): filter events by their resource's version
            timeout (int, optional):

        Returns:
            list of event objects

        Example:
            Reading all CSV Warning events in namespace "my-namespace", with reason of "AnEventReason"
              for event in Event.get(
                  default_client,
                  namespace="my-namespace",
                  field_selector="involvedObject.kind==ClusterServiceVersion,type==Warning,reason=AnEventReason",
                  timeout=10,
              ):
                print(event.object)
        """
        LOGGER.info(
            f"get events parameters: namespace={namespace}, name={name}, label_selector={label_selector}, "
            f"field_selector='{field_selector}', resource_version={resource_version}, timeout={timeout}"
        )

        event_listener = dyn_client.resources.get(
            api_version=cls.api_version, kind=cls.__name__
        )
        for event in event_listener.watch(
            namespace=namespace,
            name=name,
            label_selector=label_selector,
            field_selector=field_selector,
            resource_version=resource_version,
            timeout=timeout,
        ):
            yield event

    @classmethod
    def delete_events(
        cls,
        dyn_client,
        namespace=None,
        name=None,
        label_selector=None,
        field_selector=None,
        resource_version=None,
        timeout=None,
    ):
        """
        Deletes K8s events. For example, to cleanup events before test, in order to not get old events in
        the test, in order to prevent false positive test.

        Args:
            dyn_client (obj): K8s client
            namespace (str, optional): event namespace
            name (str, optional): event name
            label_selector (str, optional): filter events by labels; comma separated string of key=value; optional
            field_selector (str, optional): filter events by event fields; comma separated string of key=value
            resource_version (str, optional): filter events by their resource's version
            timeout (int):

        Example:
            Deleting all the event with a reason of "AnEventReason", from "my-namespace" namespace
            @pytest.fixture()
            def delete_events_before_test(default_client):
            Event.delete_events(default_client, namespace=my-namespace, field_selector="reason=AnEventReason")
        """
        LOGGER.info(
            f"delete_events parameters: namespace={namespace}, name={name}, label_selector={label_selector}, "
            f"field_selector='{field_selector}', resource_version={resource_version}, timeout={timeout}"
        )
        dyn_client.resources.get(api_version=cls.api_version, kind=cls.__name__).delete(
            namespace=namespace,
            name=name,
            label_selector=label_selector,
            field_selector=field_selector,
            resource_version=resource_version,
            timeout=timeout,
        )
