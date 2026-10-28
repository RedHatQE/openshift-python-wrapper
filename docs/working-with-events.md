Let me start by exploring the repository structure and the knowledge graph.

Now let me explore the Event-related source code:

Now let me look at the `_build_event_field_selector` function and related event test files:

Now let me check the `events` test files in the tests directory:

Now let me check the resource.py import and the `events` method more carefully, and also look at how TIMEOUT_4MINUTES is defined:

Let me check where TIMEOUT_4MINUTES is defined in resource.py:

Now let me check the constants value for TIMEOUT_4MINUTES:

Now let me check how the Event class is used in the fake client:

Now let me look at the `_extract_event_info` and the `_process_watch_events` functions to understand the event data structure better:

Now let me look at the event object structure from watch events:

Now let me check how to properly import and use Event:

Let me also look at the test file for events in more detail:

Now let me check the watch method's return structure for events:

Now I have a thorough understanding. Let me write the documentation.

# Working with Kubernetes Events

Monitor, retrieve, and clean up Kubernetes events to debug resource behavior and automate event-driven workflows using the `Event` class and the `resource.events()` method.

## Prerequisites

- A connected Kubernetes/OpenShift client — see [Connecting to Clusters](connecting-to-clusters.html)
- The `ocp_resources` package installed — see [Installing and Creating Your First Resource](quickstart.html)

## Quick Example

Stream events from a namespace in real-time:

```python
from ocp_resources.event import Event

for event in Event.get(client=client, namespace="my-namespace", timeout=30):
    print(f"{event['type']}: {event.object.reason} — {event.object.message}")
```

## Streaming Events in Real-Time with `Event.get()`

`Event.get()` opens a watch connection and yields events as they occur. It's a generator that blocks until the timeout expires or you break out of the loop.

```python
from ocp_resources.event import Event

for event in Event.get(
    client=client,
    namespace="my-namespace",
    timeout=60,
):
    obj = event.object
    print(f"[{obj.type}] {obj.reason}: {obj.message}")
```

Each yielded event is a watch event dictionary with these keys:

| Key            | Description                                                        |
|----------------|--------------------------------------------------------------------|
| `type`         | Watch event type: `ADDED`, `MODIFIED`, or `DELETED`                |
| `object`       | The Event resource object (access `.type`, `.reason`, `.message`, `.involvedObject`, etc.) |
| `raw_object`   | The raw dictionary representation of the event                     |

### `Event.get()` Parameters

| Parameter          | Type                    | Default  | Description                                               |
|--------------------|-------------------------|----------|-----------------------------------------------------------|
| `client`           | `DynamicClient`         | `None`   | Kubernetes dynamic client (required)                      |
| `namespace`        | `str \| None`           | `None`   | Filter events to a specific namespace                     |
| `name`             | `str \| None`           | `None`   | Filter by event name                                      |
| `label_selector`   | `str \| None`           | `None`   | Filter by labels (e.g. `"app=nginx"`)                     |
| `field_selector`   | `str \| None`           | `None`   | Filter by fields (e.g. `"type==Warning"`)                 |
| `resource_version` | `str \| None`           | `None`   | Start watching from a specific resource version           |
| `timeout`          | `int \| None`           | `None`   | Timeout in seconds; `None` watches indefinitely           |

**Returns:** `Generator` — yields watch event dictionaries.

### Filtering with Field Selectors

Field selectors let you narrow down events to exactly what you care about. Combine multiple selectors with commas:

```python
# Only Warning events for ClusterServiceVersion resources
for event in Event.get(
    client=client,
    namespace="my-namespace",
    field_selector="involvedObject.kind==ClusterServiceVersion,type==Warning,reason==AnEventReason",
    timeout=10,
):
    print(event.object.message)
```

Common field selector fields:

| Field                        | Example                                        |
|------------------------------|-------------------------------------------------|
| `type`                       | `type==Warning` or `type==Normal`               |
| `reason`                     | `reason==FailedScheduling`                      |
| `involvedObject.kind`        | `involvedObject.kind==Pod`                      |
| `involvedObject.name`        | `involvedObject.name==my-pod`                   |
| `involvedObject.namespace`   | `involvedObject.namespace==default`             |

## Listing Existing Events with `Event.list()`

Unlike `Event.get()`, which streams events in real-time, `Event.list()` returns existing events immediately as a list. By default it only returns events from the last 5 minutes.

```python
from ocp_resources.event import Event

# List all Warning events from the last 5 minutes
events = Event.list(
    client=client,
    namespace="my-namespace",
    field_selector="type==Warning",
)

for event in events:
    print(f"{event.reason}: {event.message}")
```

Results are sorted by `lastTimestamp` descending (most recent first).

### `Event.list()` Parameters

| Parameter        | Type                | Default | Description                                               |
|------------------|---------------------|---------|-----------------------------------------------------------|
| `client`         | `DynamicClient`     | —       | Kubernetes dynamic client (required)                      |
| `namespace`      | `str \| None`       | `None`  | Filter events to a specific namespace                     |
| `field_selector` | `str \| None`       | `None`  | Filter by fields (e.g. `"type==Warning"`)                 |
| `label_selector` | `str \| None`       | `None`  | Filter by labels                                          |
| `since_seconds`  | `int`               | `300`   | Only return events from the last N seconds                |

**Returns:** `list` — event resource objects sorted by timestamp (most recent first).

**Raises:** `ValueError` — if `since_seconds` is negative.

```python
# Events from the last 30 minutes
events = Event.list(client=client, since_seconds=1800)

# All events (no time filter — uses a very large window)
events = Event.list(client=client, since_seconds=999999)
```

### When to Use `Event.get()` vs `Event.list()`

| Use case                                         | Method         |
|--------------------------------------------------|----------------|
| Watch for new events as they happen               | `Event.get()`  |
| Fetch events that already occurred                | `Event.list()` |
| Collect events during a test run                  | `Event.get()`  |
| Check recent events after a failure               | `Event.list()` |
| Stream events with a timeout                      | `Event.get()`  |
| Get a snapshot sorted by time                     | `Event.list()` |

## Getting Events for a Specific Resource

Every resource instance has an `.events()` method that automatically filters events to that specific resource by setting `involvedObject.name` in the field selector.

```python
from ocp_resources.pod import Pod

pod = Pod(client=client, name="my-pod", namespace="default")

for event in pod.events(timeout=10):
    print(f"{event.object.reason}: {event.object.message}")
```

You can add extra filters on top of the automatic resource filter:

```python
# Only Warning events for this specific pod
for event in pod.events(
    field_selector="type==Warning",
    timeout=10,
):
    print(event.object.message)
```

### `resource.events()` Parameters

| Parameter          | Type    | Default | Description                                               |
|--------------------|---------|---------|-----------------------------------------------------------|
| `name`             | `str`   | `""`    | Filter by event name                                      |
| `label_selector`   | `str`   | `""`    | Filter by labels                                          |
| `field_selector`   | `str`   | `""`    | Additional field selectors (combined with `involvedObject.name` automatically) |
| `resource_version` | `str`   | `""`    | Start watching from a specific resource version           |
| `timeout`          | `int`   | `240`   | Timeout in seconds (default: 4 minutes)                   |

**Returns:** `Generator` — yields watch event dictionaries, same format as `Event.get()`.

> **Note:** The `field_selector` you provide is appended to the automatic `involvedObject.name==<resource-name>` filter. You don't need to specify the resource name yourself.

## Deleting Events with `Event.delete_events()`

Clean up events before a test run to avoid false positives from stale events:

```python
from ocp_resources.event import Event

# Delete all events in a namespace
Event.delete_events(client=client, namespace="my-namespace")

# Delete events matching a specific reason
Event.delete_events(
    client=client,
    namespace="my-namespace",
    field_selector="reason==AnEventReason",
)
```

### `Event.delete_events()` Parameters

| Parameter          | Type                    | Default  | Description                                               |
|--------------------|-------------------------|----------|-----------------------------------------------------------|
| `client`           | `DynamicClient`         | `None`   | Kubernetes dynamic client (required)                      |
| `namespace`        | `str \| None`           | `None`   | Target namespace                                          |
| `name`             | `str \| None`           | `None`   | Specific event name to delete                             |
| `label_selector`   | `str \| None`           | `None`   | Filter by labels                                          |
| `field_selector`   | `str \| None`           | `None`   | Filter by fields                                          |
| `resource_version` | `str \| None`           | `None`   | Filter by resource version                                |
| `timeout`          | `int \| None`           | `None`   | Timeout in seconds                                        |

**Returns:** `None`

## Advanced Usage

### Test Setup: Clean Events Before Each Test

A common pattern is deleting events before a test so that only events generated during the test are captured:

```python
from ocp_resources.event import Event


def test_pod_scheduling(client, namespace):
    # Clean slate — remove old events
    Event.delete_events(client=client, namespace=namespace)

    # ... create resources and trigger the behavior under test ...

    # Verify expected events occurred
    events = Event.list(
        client=client,
        namespace=namespace,
        field_selector="reason==Scheduled",
        since_seconds=60,
    )
    assert len(events) > 0, "Pod was not scheduled"
```

### Collecting Events During an Operation

Use `Event.get()` with a timeout to capture all events that occur during an operation:

```python
from ocp_resources.event import Event

events = []
for event in Event.get(
    client=client,
    namespace="my-namespace",
    field_selector="involvedObject.kind==Deployment",
    timeout=30,
):
    events.append(event.object)
    if event.object.reason == "ScalingReplicaSet":
        break  # Found what we were looking for

print(f"Captured {len(events)} events")
```

### Watching Cluster-Wide Events

Omit the `namespace` parameter to watch events across all namespaces:

```python
from ocp_resources.event import Event

# Watch all Warning events cluster-wide
for event in Event.get(
    client=client,
    field_selector="type==Warning",
    timeout=60,
):
    ns = event.object.involvedObject.get("namespace", "cluster-scoped")
    print(f"[{ns}] {event.object.reason}: {event.object.message}")
```

### Accessing Event Object Properties

The `event.object` yielded by `Event.get()` and `resource.events()` is a Kubernetes `ResourceInstance` with these commonly used attributes:

| Attribute                     | Description                                  |
|-------------------------------|----------------------------------------------|
| `event.object.type`           | `"Normal"` or `"Warning"`                    |
| `event.object.reason`         | Short reason string (e.g. `"Scheduled"`)     |
| `event.object.message`        | Human-readable event message                 |
| `event.object.count`          | Number of times this event occurred          |
| `event.object.firstTimestamp`  | When the event first occurred                |
| `event.object.lastTimestamp`   | When the event most recently occurred        |
| `event.object.source`         | Dict with `component` and `host`             |
| `event.object.involvedObject` | Dict with `kind`, `name`, `namespace`, etc.  |

## Troubleshooting

**`Event.get()` hangs indefinitely**
You likely omitted the `timeout` parameter. Always set a `timeout` value to avoid blocking forever:

```python
# Bad — hangs if no events arrive
for event in Event.get(client=client, namespace="ns"):
    ...

# Good — stops after 30 seconds
for event in Event.get(client=client, namespace="ns", timeout=30):
    ...
```

**`Event.list()` returns an empty list**
- Check the `since_seconds` value. The default is 300 (5 minutes). If the events are older, increase the value.
- Verify the `namespace` is correct.
- Ensure the `field_selector` syntax uses `==` (double equals), not `=`.

**`resource.events()` returns events for other resources too**
This method filters only by `involvedObject.name`. If multiple resources share the same name across different kinds, add a `field_selector` to narrow it down:

```python
for event in pod.events(
    field_selector="involvedObject.kind==Pod",
    timeout=10,
):
    print(event.object.message)
```

> **Warning:** The `dyn_client` parameter on `Event.get()` and `Event.delete_events()` is deprecated and will be removed in the next major release. Use `client` instead.

## Related Pages

- [Querying and Watching Resources](querying-resources.html)
- [Common Resource Patterns](common-patterns.html)
- [Executing Commands in Pods and Retrieving Logs](pod-execution-and-logs.html)
- [Waiting for Resource Conditions and Status](waiting-for-conditions.html)
- [Creating and Managing Resources](creating-and-managing-resources.html)
