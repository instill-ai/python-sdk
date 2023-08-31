"""Sample integration test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned


from instill_sdk.client import MgmtClient


def describe_client():
    def describe_host():
        test_client = MgmtClient()

        def when_not_set(expect):
            test_client = MgmtClient()
            expect(test_client.host) == "localhost"

        def when_set_correct_type(expect):
            test_client = MgmtClient()
            test_client.host = "123"
            expect(test_client.host) == "123"

    def describe_protocol():
        test_client = MgmtClient()

        def when_not_set(expect):
            test_client = MgmtClient()
            expect(test_client.protocol) == "http"

        def when_set_correct_type(expect):
            test_client = MgmtClient()
            test_client.protocol = "123"
            expect(test_client.protocol) == "123"

    def describe_port():
        def when_not_set(expect):
            test_client = MgmtClient()
            expect(test_client.port) == "7080"

        def when_set_correct_type(expect):
            test_client = MgmtClient()
            test_client.port = "123"
            expect(test_client.port) == "123"
