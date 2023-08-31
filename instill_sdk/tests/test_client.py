"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

from instill_sdk import client


def set_and_get_host_to_client():
    def when_set(expect):
        test_client = client.MgmtClient
        test_client.host = "123"  # type: ignore
        expect(test_client.host) == "123"

    def when_not_set(expect):
        test_client = client.MgmtClient
        expect(test_client.host) == "localhost"
