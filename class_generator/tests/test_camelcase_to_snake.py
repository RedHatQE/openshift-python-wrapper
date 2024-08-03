import pytest

from class_generator.class_generator import (
    convert_camel_case_to_snake_case,
)


@pytest.mark.parametrize(
    "camel_case_str, expected",
    [
        pytest.param("Title", "title", id="title_word"),
        pytest.param("tolerations", "tolerations", id="lowercase_word"),
        pytest.param("UPPERCASEWORD", "uppercaseword", id="uppercase_word"),
        pytest.param("ipFamilies", "ip_families", id="combined_basic_with_two_words"),
        pytest.param(
            "allocateLoadBalancerNodePorts",
            "allocate_load_balancer_node_ports",
            id="combined_basic_with_multiple_words",
        ),
        pytest.param("XMLHttpRequest", "xml_http_request", id="combined_uppercase_word_is_first"),
        pytest.param(
            "additionalCORSAllowedOS",
            "additional_cors_allowed_os",
            id="combined_uppercase_word_in_the_middle",
        ),
        pytest.param("hostIPC", "host_ipc", id="combined_uppercase_word_is_last"),
        pytest.param(
            "clusterIPs",
            "cluster_ips",
            id="combined_uppercase_word_is_last_ends_with_one_lowercase_char",
        ),
        pytest.param(
            "dataVolumeTTLSeconds",
            "data_volume_ttl_seconds",
            id="combined_uppercase_word_followed_by_uppercase_word_is_last_ends_with_lowercase",
        ),
    ],
)
def test_convert_camel_case_to_snake_case(camel_case_str, expected):
    assert convert_camel_case_to_snake_case(string_=camel_case_str) == expected
