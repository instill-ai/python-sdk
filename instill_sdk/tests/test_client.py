"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison
from instill_sdk.clients.mgmt import MgmtClient


def set_and_get_instance_to_client():
    def when_set(expect):
        test_client = MgmtClient()
        test_client.instance = "test"
        expect(test_client.instance) == "test"

    def when_not_set(expect):
        test_client = MgmtClient()
        expect(test_client.instance) == "default"
