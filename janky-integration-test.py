# pylint: disable=no-member,no-name-in-module
import requests
import base64

from google.protobuf.struct_pb2 import Struct
from instill.clients import get_client
from instill.resources.model import GithubModel

from instill.resources.connector_ai import InstillModelConnector
from instill.resources.connector import Connector
from instill.resources.pipeline import Pipeline
import instill.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill.protogen.vdp.connector.v1alpha.connector_pb2 as connector_interface
import instill.protogen.vdp.pipeline.v1alpha.pipeline_pb2 as pipeline_interface
import instill.protogen.model.model.v1alpha.task_classification_pb2 as classification
from instill.utils.logger import Logger

local_model = {
    "model_name": "test1",
    "model_description": "test1",
    "model_path": "/Users/heiru/Projects/instill/model-backend/integration-test/data/dummy-cls-model.zip",
}
github_model = {
    "model_name": "yolov7",
    "model_repo": "instill-ai/model-yolov7-dvc",
    "model_tag": "v1.0-cpu",
}

try:
    client = get_client()

    # ================================================================================================================
    # ===================================================== mgmt =====================================================
    assert client.mgmt_service.is_serving()
    Logger.i("mgmt client created, assert status == serving: True")

    user = client.mgmt_service.get_user()
    assert user.id == "admin"
    Logger.i("mgmt get user, assert default user id == admin: True")

    # ================================================================================================================
    # ===================================================== model ====================================================
    assert client.model_serevice.is_serving()
    Logger.i("model client created, assert status == serving: True")

    model = GithubModel(
        client=client,
        name=github_model["model_name"],
        model_repo=github_model["model_repo"],
        model_tag=github_model["model_tag"],
    )

    assert model.get_state() == model_interface.Model.STATE_OFFLINE
    Logger.i("model created, assert STATE_OFFLINE: True")

    model.deploy()
    assert model.get_state() == model_interface.Model.STATE_ONLINE
    Logger.i("model deployed, assert STATE_ONLINE: True")

    task_inputs = [
        model_interface.TaskInput(
            classification=classification.ClassificationInput(
                image_url="https://artifacts.instill.tech/imgs/dog.jpg"
            )
        ),
        model_interface.TaskInput(
            classification=classification.ClassificationInput(
                image_url="https://artifacts.instill.tech/imgs/bear.jpg"
            )
        ),
        model_interface.TaskInput(
            classification=classification.ClassificationInput(
                image_url="https://artifacts.instill.tech/imgs/polar-bear.jpg"
            )
        ),
    ]

    outputs = model(task_inputs=task_inputs)
    assert outputs[0].detection.objects[0].category == "dog"
    Logger.i("inference done, assert output 0 object 0 category == dog: True")
    assert outputs[0].detection.objects[1].category == "dog"
    Logger.i("inference done, assert output 0 object 1 category == dog: True")
    assert outputs[1].detection.objects[0].category == "bear"
    Logger.i("inference done, assert output 1 category == bear: True")
    assert outputs[2].detection.objects[0].category == "bear"
    Logger.i("inference done, assert output 2 category == bear: True")

    # ================================================================================================================
    # ================================================== connector ===================================================
    assert client.connector_service.is_serving()
    Logger.i("connector client created, assert status == serving: True")

    instill_connector = InstillModelConnector(
        client,
        name="instill",
        server_url="http://api-gateway:8080",
    )
    assert (
        instill_connector.get_state()
        == connector_interface.ConnectorResource.STATE_DISCONNECTED
    )
    Logger.i(
        "instill model connector created, assert state == STATE_DISCONNECTED: True"
    )

    assert (
        instill_connector.test()
        == connector_interface.ConnectorResource.STATE_CONNECTED
    )
    Logger.i("instill model connector, assert state == STATE_CONNECTED: True")

    config = {"destination_path": "/local/test-1"}
    csv_connector = Connector(
        client,
        name="csv",
        definition="connector-definitions/airbyte-destination-csv",
        configuration=config,
    )
    assert (
        csv_connector.get_state()
        == connector_interface.ConnectorResource.STATE_DISCONNECTED
    )
    Logger.i("csv connector created, assert state == STATE_DISCONNECTED: True")

    assert csv_connector.test() == connector_interface.ConnectorResource.STATE_CONNECTED
    Logger.i("tested csv connector, assert state == STATE_CONNECTED: True")

    # ================================================================================================================
    # ================================================= csv pipeline =================================================
    assert client.pipeline_service.is_serving()
    Logger.i("pipeline client created, assert status == serving: True")

    start_operator_component = pipeline_interface.Component()
    start_operator_component.id = "start"
    start_operator_component.definition_name = "operator-definitions/start-operator"
    start_operator_component.configuration.update(
        {"metadata": {"input": {"title": "Input", "type": "text"}}}
    )
    end_operator_component = pipeline_interface.Component()
    end_operator_component.id = "end"
    end_operator_component.definition_name = "operator-definitions/end-operator"
    end_operator_component.configuration.update(
        {
            "metadata": {"answer": {"title": "Answer"}},
            "input": {"answer": "{ d01.input }"},
        }
    )
    csv_connector_component = pipeline_interface.Component()
    csv_connector_component.id = "d01"
    csv_connector_component.resource_name = f"{user.name}/connector-resources/csv"
    csv_connector_component.definition_name = (
        "connector-definitions/airbyte-destination-csv"
    )
    csv_connector_component.configuration.update({"input": {"text": "{ start.input }"}})

    recipe = pipeline_interface.Recipe()
    recipe.version = "v1alpha"
    recipe.components.append(start_operator_component)
    recipe.components.append(end_operator_component)
    recipe.components.append(csv_connector_component)

    csv_pipeline = Pipeline(client=client, name="csv-pipeline", recipe=recipe)
    csv_pipeline.validate_pipeline()
    Logger.i("csv-pipeline created, validate without error: True")
    i = Struct()
    i.update({"input": "instill-ai rocks"})
    assert csv_pipeline([i])[0][0]["answer"]["text"] == "instill-ai rocks"
    Logger.i("csv-pipeline triggered, output matched input: True")

    # =================================================================================================================
    # ============================================= instill model pipeline ============================================
    start_operator_component = pipeline_interface.Component()
    start_operator_component.id = "start"
    start_operator_component.definition_name = "operator-definitions/start-operator"
    start_operator_component.configuration.update(
        {"metadata": {"input": {"title": "input", "type": "image"}}}
    )
    instill_model_connector_component = pipeline_interface.Component()
    instill_model_connector_component.id = "yolov7"
    instill_model_connector_component.resource_name = (
        f"{user.name}/connector-resources/instill"
    )
    instill_model_connector_component.definition_name = (
        instill_connector.get_definition().name
    )
    instill_model_connector_component.configuration.update(
        {
            "input": {
                "task": "TASK_DETECTION",
                "image_base64": "{ start.input }",
                "model_name": "users/admin/models/yolov7",
            },
        }
    )

    end_operator_component = pipeline_interface.Component()
    end_operator_component.id = "end"
    end_operator_component.definition_name = "operator-definitions/end-operator"
    end_operator_component.configuration.update(
        {"input": {"output": "{ yolov7.output.objects }"}, "metadata": {"output": {}}}
    )

    recipe = pipeline_interface.Recipe()
    recipe.version = "v1alpha"
    recipe.components.append(start_operator_component)
    recipe.components.append(instill_model_connector_component)
    recipe.components.append(end_operator_component)
    instill_model_pipeline = Pipeline(
        client=client, name="instill-model-pipeline", recipe=recipe
    )
    instill_model_pipeline.validate_pipeline()
    Logger.i("instill-model-pipeline created, validate without error: True")
    i = Struct()
    i.update(
        {
            "input": base64.b64encode(
                requests.get(
                    "https://artifacts.instill.tech/imgs/dog.jpg", timeout=5
                ).content
            ).decode("ascii")
        }
    )

    assert instill_model_pipeline([i])[0][0]["output"][0]["category"] == "dog"
    Logger.i("instill-model-pipeline triggered, output matched input: True")
except AssertionError:
    Logger.w("TEST FAILED, ASSERTION MISMATCHED")

Logger.i("====================Test Done====================")
Logger.i("===================Cleaning up===================")
del csv_pipeline
del instill_model_pipeline
del model
del instill_connector
del csv_connector
