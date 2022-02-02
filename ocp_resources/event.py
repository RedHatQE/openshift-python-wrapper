from ocp_resources.logger import get_logger
from ocp_resources.resource import Resource


LOGGER = get_logger(name=__name__)


class Event:
    """
    Allow read and remove K8s events.
    """

    api_version = Resource.ApiVersion.V1

    @classmethod
    def get(
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
        get - retrieves K8s events.
        :param dyn_client: K8s client; mandatory
        :param namespace: event namespace; optional
        :param name: event name; optional
        :param label_selector: filter events by labels; comma separated string of key=value; optional
        :param field_selector: filter events by event fields; comma separated string of key=value; optional
        :param resource_version: filter events by their resource's version; optional
        :param timeout: timeout; optional
        :return: list of event objects

        example: reading all CSV Warning events in namespace "my-namespace", with reason of "AnEventReason"
              for event in Event.get(
                  default_client,
                  namespace="my-namespace",
                  field_selector="involvedObject.kind==ClusterServiceVersion,type==Warning,reason=AnEventReason",
                  timeout=10,
              ):
                print(event.object)
        """

        LOGGER.info("Reading events")
        LOGGER.debug(
            f"get events parameters: namespace={namespace}, name={name}, label_selector={label_selector}, "
            f"field_selector='{field_selector}', resource_version={resource_version}, timeout={timeout}"
        )

        event_listener = dyn_client.resources.get(
            api_version=cls.api_version, kind=cls.__name__
        )
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
        dyn_client,
        namespace=None,
        name=None,
        label_selector=None,
        field_selector=None,
        resource_version=None,
        timeout=None,
    ):
        """
        delete_events - delete K8s events. For example, to cleanup events before test, in order to not get old events in
                        the test, in order to prevent false positive test.
        :param dyn_client: K8s client; mandatory
        :param namespace: event namespace; optional
        :param name: event name; optional
        :param label_selector: filter events by labels; comma separated string of key=value; optional
        :param field_selector: filter events by event fields; comma separated string of key=value; optional
        :param resource_version: filter events by their resource's version; optional
        :param timeout: timeout; optional
        :return: list of event objects

        example: deleting all the event with a reason of "AnEventReason", from "my-namespace" namespace

        @pytest.fixture()
        def delete_events_before_test(default_client):
          Event.delete_events(default_client, namespace=my-namespace, field_selector="reason=AnEventReason")
        """
        LOGGER.info("Deleting events")
        LOGGER.debug(
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
