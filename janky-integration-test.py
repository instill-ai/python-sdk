# pylint: disable=no-member, no-name-in-module
from google.protobuf.struct_pb2 import Struct
from instill_sdk.clients.mgmt import MgmtClient
from instill_sdk.clients.model import ModelClient
from instill_sdk.clients.connector import ConnectorClient
from instill_sdk.clients.pipeline import PipelineClient
from instill_sdk.resources.model import GithubModel

# from instill_sdk.resources.connector_ai import InstillModelConnector
from instill_sdk.resources.connector import Connector
from instill_sdk.resources.pipeline import Pipeline
import instill_sdk.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill_sdk.protogen.vdp.connector.v1alpha.connector_pb2 as connector_interface
import instill_sdk.protogen.vdp.pipeline.v1alpha.pipeline_pb2 as pipeline_interface
import instill_sdk.protogen.model.model.v1alpha.task_classification_pb2 as classification
from instill_sdk.utils.logger import Logger

local_model = {
    "model_name": "test1",
    "model_description": "test1",
    "model_path": "/Users/heiru/Projects/instill/model-backend/integration-test/data/dummy-cls-model.zip",
}
github_model = {
    "model_name": "mobilenetv2",
    "model_repo": "instill-ai/model-mobilenetv2-dvc",
    "model_tag": "v1.0-cpu",
}

try:
    # ======================== mgmt

    c = MgmtClient()
    assert c.is_serving()
    Logger.i("mgmt client created, assert status == serving: True")

    user = c.get_user()
    assert user.id == "instill-ai"
    Logger.i("mgmt get user, assert default user id == instill-ai: True")
except AssertionError:
    pass
try:
    # ======================== model

    m = ModelClient(user=user)
    assert m.is_serving()
    Logger.i("model client created, assert status == serving: True")

    model = GithubModel(
        client=m,
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
    assert outputs[0].classification.category == "golden retriever"
    Logger.i("inference done, assert output 0 category == golden retriever: True")
    assert outputs[1].classification.category == "brown bear"
    Logger.i("inference done, assert output 1 category == brown bear: True")
    assert outputs[2].classification.category == "ice bear"
    Logger.i("inference done, assert output 2 category == ice bear: True")
except AssertionError:
    for model in m.list_models():
        m.delete_model(model.id)
try:
    # ======================== connector

    co = ConnectorClient(user=user)
    assert co.is_serving()
    Logger.i("connector client created, assert status == serving: True")

    # mobilenet_connector = InstillModelConnector(co, "mobilenetv2_connector", "", "http://model-backend:9080", "mobilenetv2")
    config = {"destination_path": "/local/pipeline-backend-test-1"}
    csv_connector = Connector(
        co,
        name="csv",
        definition="connector-definitions/airbyte-destination-csv",
        configuration=config,
    )
    assert (
        csv_connector.get_state()
        == connector_interface.ConnectorResource.STATE_DISCONNECTED
    )
    Logger.i("csv connector created, assert state == STATE_DISCONNECTED: True")

    csv_connector.connect()
    assert (
        csv_connector.get_state()
        == connector_interface.ConnectorResource.STATE_CONNECTED
    )
    Logger.i("csv connector connected, assert state == STATE_CONNECTED: True")

    assert csv_connector.test() == connector_interface.ConnectorResource.STATE_CONNECTED
    Logger.i("tested csv connector, assert state == STATE_CONNECTED: True")
except AssertionError:
    for model in m.list_models():
        m.delete_model(model.id)
    for connector in co.list_connectors():
        co.delete_connector(connector.id)
try:
    # ======================== pipeline

    p = PipelineClient(user=user)
    assert p.is_serving()
    Logger.i("pipeline client created, assert status == serving: True")

    start_operator_component = pipeline_interface.Component()
    start_operator_component.id = "start"
    start_operator_component.definition_name = "operator-definitions/start-operator"
    start_operator_component.configuration.update(
        {"metadata": {"body": {"input": {"title": "Input", "type": "text"}}}}
    )
    end_operator_component = pipeline_interface.Component()
    end_operator_component.id = "end"
    end_operator_component.definition_name = "operator-definitions/end-operator"
    end_operator_component.configuration.update(
        {
            "metadata": {
                "body": {"output": {"title": "output"}},
            },
            "input": {"body": {"output": "{ start.body.input }"}},
        }
    )
    csv_connector_component = pipeline_interface.Component()
    csv_connector_component.id = "d01"
    csv_connector_component.resource_name = f"{user.name}/connector-resources/csv"
    csv_connector_component.definition_name = (
        "connector-definitions/airbyte-destination-csv"
    )
    csv_connector_component.configuration.update(
        {"input": {"text": "{ start.body.input }"}}
    )

    recipe = pipeline_interface.Recipe()
    recipe.version = "v1alpha"
    recipe.components.append(start_operator_component)
    recipe.components.append(end_operator_component)
    recipe.components.append(csv_connector_component)

    pipeline = Pipeline(client=p, name="csv-pipeline", recipe=recipe)
    pipeline.validate_pipeline()
    Logger.i("pipeline csv-pipeline created, validate without error: True")
    i = Struct()
    i.update({"input": "instill-ai rocks"})
    assert pipeline([i])[0][0]["output"] == "instill-ai rocks"
    Logger.i("pipeline csv-pipeline triggered, output matched input: True")
except AssertionError:
    pass
# ======================== clean up
for pipeline in p.list_pipelines():
    p.delete_pipeline(pipeline.id)
for connector in co.list_connectors():
    co.delete_connector(connector.id)
for model in m.list_models():
    m.delete_model(model.id)
