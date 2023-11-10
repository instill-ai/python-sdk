# pylint: disable=no-member,no-name-in-module
import base64
import requests

from google.protobuf.struct_pb2 import Struct
from instill.clients import get_client
from instill.resources.model import GithubModel

from instill.resources import (
    Connector,
    InstillModelConnector,
    OpenAIConnector,
    StabilityAIConnector,
    Pipeline,
    model_pb,
    connector_pb,
    task_detection,
    task_classification,
    create_start_operator,
    create_end_operator,
    create_recipe,
)

from instill.utils.logger import Logger

local_model = {
    "model_name": "test1",
    "model_description": "test1",
    "model_path": "/Users/heiru/Projects/instill/model-backend/integration-test/data/dummy-cls-model.zip",
}
yolov7_config = {
    "model_name": "yolov7",
    "model_repo": "instill-ai/model-yolov7-dvc",
    "model_tag": "v1.0-cpu",
}

mobilenetv2_config = {
    "model_name": "mobilenetv2",
    "model_repo": "instill-ai/model-mobilenetv2-dvc",
    "model_tag": "v1.0-cpu",
}

try:
    client = get_client()

    Logger.i(
        "==================== mgmt =========================================================================="
    )
    assert client.mgmt_service.is_serving()
    Logger.i("mgmt client created, assert status == serving: True")

    user = client.mgmt_service.get_user()
    assert user.id == "admin"
    Logger.i("mgmt get user, assert default user id == admin: True")

    Logger.i(
        "==================== model ========================================================================="
    )
    assert client.model_service.is_serving()
    Logger.i("model client created, assert status == serving: True")

    Logger.i(
        "==================== yolov7 model =================================================================="
    )

    yolov7 = GithubModel(
        client=client,
        name=yolov7_config["model_name"],
        model_repo=yolov7_config["model_repo"],
        model_tag=yolov7_config["model_tag"],
    )

    assert yolov7.get_state() == model_pb.Model.STATE_OFFLINE
    Logger.i("yolov7 created, assert STATE_OFFLINE: True")

    yolov7.deploy()
    assert yolov7.get_state() == model_pb.Model.STATE_ONLINE
    Logger.i("yolov7 deployed, assert STATE_ONLINE: True")

    task_inputs = [
        model_pb.TaskInput(
            detection=task_detection.DetectionInput(
                image_url="https://artifacts.instill.tech/imgs/dog.jpg"
            )
        ),
        model_pb.TaskInput(
            detection=task_detection.DetectionInput(
                image_url="https://artifacts.instill.tech/imgs/bear.jpg"
            )
        ),
        model_pb.TaskInput(
            detection=task_detection.DetectionInput(
                image_url="https://artifacts.instill.tech/imgs/polar-bear.jpg"
            )
        ),
    ]

    outputs = yolov7(task_inputs=task_inputs)
    assert outputs[0].detection.objects[0].category == "dog"
    Logger.i("inference done, assert output 0 object 0 category == dog: True")
    assert outputs[0].detection.objects[1].category == "dog"
    Logger.i("inference done, assert output 0 object 1 category == dog: True")
    assert outputs[1].detection.objects[0].category == "bear"
    Logger.i("inference done, assert output 1 category == bear: True")
    assert outputs[2].detection.objects[0].category == "bear"
    Logger.i("inference done, assert output 2 category == bear: True")

    Logger.i(
        "==================== mobilenetv2 model ============================================================="
    )

    mobilenet = GithubModel(
        client=client,
        name=mobilenetv2_config["model_name"],
        model_repo=mobilenetv2_config["model_repo"],
        model_tag=mobilenetv2_config["model_tag"],
    )

    assert mobilenet.get_state() == model_pb.Model.STATE_OFFLINE
    Logger.i("mobilenet created, assert STATE_OFFLINE: True")

    mobilenet.deploy()
    assert mobilenet.get_state() == model_pb.Model.STATE_ONLINE
    Logger.i("mobilenet deployed, assert STATE_ONLINE: True")

    task_inputs = [
        model_pb.TaskInput(
            classification=task_classification.ClassificationInput(
                image_url="https://artifacts.instill.tech/imgs/dog.jpg"
            )
        ),
    ]

    outputs = mobilenet(task_inputs=task_inputs)
    assert outputs[0].classification.category == "golden retriever"
    Logger.i("inference done, assert output 0 category == golden retriever: True")

    Logger.i(
        "==================== connector ====================================================================="
    )
    assert client.connector_service.is_serving()
    Logger.i("connector client created, assert status == serving: True")

    Logger.i(
        "==================== instill model connector ======================================================="
    )

    instill_connector = InstillModelConnector(
        client,
        name="instill",
        server_url="http://api-gateway:8080",
    )
    assert (
        instill_connector.get_state()
        == connector_pb.ConnectorResource.STATE_DISCONNECTED
    )
    Logger.i(
        "instill model connector created, assert state == STATE_DISCONNECTED: True"
    )

    assert instill_connector.test() == connector_pb.ConnectorResource.STATE_CONNECTED
    Logger.i("test instill model connector, assert state == STATE_CONNECTED: True")

    Logger.i(
        "==================== openai connector =============================================================="
    )

    openai_connector = OpenAIConnector(
        client,
        name="openai",
        api_key="",
    )
    assert (
        openai_connector.get_state()
        == connector_pb.ConnectorResource.STATE_DISCONNECTED
    )
    Logger.i("openai connector created, assert state == STATE_DISCONNECTED: True")

    assert openai_connector.test() == connector_pb.ConnectorResource.STATE_CONNECTED
    Logger.i("test openai connector, assert state == STATE_CONNECTED: True")

    Logger.i(
        "==================== stability ai connector ========================================================"
    )

    stability_connector = StabilityAIConnector(
        client,
        name="stabilityai",
        api_key="",
    )
    assert (
        stability_connector.get_state()
        == connector_pb.ConnectorResource.STATE_DISCONNECTED
    )
    Logger.i("stability ai connector created, assert state == STATE_DISCONNECTED: True")

    assert stability_connector.test() == connector_pb.ConnectorResource.STATE_CONNECTED
    Logger.i("test stability ai connector, assert state == STATE_CONNECTED: True")

    Logger.i(
        "==================== csv connector ================================================================="
    )

    config = {"destination_path": "/local/test"}
    csv_connector = Connector(
        client,
        name="csv",
        definition="connector-definitions/airbyte-destination-csv",
        configuration=config,
    )
    assert (
        csv_connector.get_state() == connector_pb.ConnectorResource.STATE_DISCONNECTED
    )
    Logger.i("csv connector created, assert state == STATE_DISCONNECTED: True")

    assert csv_connector.test() == connector_pb.ConnectorResource.STATE_CONNECTED
    Logger.i("tested csv connector, assert state == STATE_CONNECTED: True")

    Logger.i(
        "==================== pipeline ======================================================================"
    )

    assert client.pipeline_service.is_serving()
    Logger.i("pipeline client created, assert status == serving: True")

    Logger.i(
        "==================== csv pipeline =================================================================="
    )

    start_operator_component = create_start_operator(
        config={"metadata": {"input": {"title": "Input", "type": "string", "instillFormat": "string"}}}
    )

    end_operator_component = create_end_operator(
        config={
            "metadata": {"answer": {"title": "Answer"}},
            "input": {"answer": "{ d01.input }"},
        }
    )

    csv_connector_component = csv_connector.create_component(
        name="d01", config={"input": {"data": {"text": "{ start.input }"}}}
    )

    recipe = create_recipe(
        [start_operator_component, end_operator_component, csv_connector_component]
    )

    csv_pipeline = Pipeline(client=client, name="csv-pipeline", recipe=recipe)
    csv_pipeline.validate_pipeline()
    Logger.i("csv-pipeline created, validate without error: True")
    i = Struct()
    i.update({"input": "instill-ai rocks"})
    assert csv_pipeline([i])[0][0]["answer"]["data"]["text"] == "instill-ai rocks"
    Logger.i("csv-pipeline triggered, output matched input: True")

    Logger.i(
        "==================== instill model + csv pipeline =================================================="
    )
    start_operator_component = create_start_operator(
        {"metadata": {"input": {"title": "input", "type": "string", "instillFormat": "image/*"}}}
    )

    instill_model_connector_component = instill_connector.create_component(
        name="yolov7",
        config={
            "input": {
                "image_base64": "{ start.input }",
                "model_namespace": "admin",
                "model_id": "yolov7",
            },
            "task": "TASK_DETECTION",
        },
    )

    csv_connector_component = csv_connector.create_component(
        name="csv", config={"input": {"data": {"text": "{{ yolov7.output.objects }}"}}}
    )

    end_operator_component = create_end_operator(
        config={
            "input": {"output": "{ yolov7.output.objects }"},
        }
    )

    recipe = create_recipe(
        [
            start_operator_component,
            instill_model_connector_component,
            csv_connector_component,
            end_operator_component,
        ]
    )
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

    Logger.i(
        "==================== cute pipeline ================================================================="
    )

    start_operator_component = create_start_operator(
        {"metadata": {"input": {"title": "input", "type": "array", "instillFormat": "array:image/*", "items": {"type":"string"}}}}
    )

    instill_model_component_mobilenet_1 = instill_connector.create_component(
        name="m1",
        config={
            "input": {
                "image_base64": "{ start.input[0] }",
                "model_namespace": "admin",
                "model_id": "mobilenetv2",
            },
            "task": "TASK_CLASSIFICATION",
        },
    )

    instill_model_component_mobilenet_2 = instill_connector.create_component(
        name="m2",
        config={
            "input": {
                "image_base64": "{ start.input[1] }",
                "model_namespace": "admin",
                "model_id": "mobilenetv2",
            },
            "task": "TASK_CLASSIFICATION",
        },
    )

    openai_component = openai_connector.create_component(
        name="gpt",
        config={
            "input": {
                "prompt": "{{ m1.output.category }} and {{ m2.output.category }}",
                "model": "gpt-3.5-turbo",
                "system_message": "Write a cute and upbeat story about friendship between the following two animals",
                "temperature": 0.7,
                "n": 1,
                "max_tokens": 128,
            },
            "task": "TASK_TEXT_GENERATION",
        },
    )

    stability_ai_component = stability_connector.create_component(
        name="sd",
        config={
            "input": {
                "engine": "stable-diffusion-xl-1024-v1-0",
                "prompts": "{ gpt.output.texts }",
                "style_preset": "comic-book",
                "width": 896,
                "height": 1152,
            },
            "task": "TASK_TEXT_TO_IMAGE",
        },
    )

    end_operator_component = create_end_operator(
        config={
            "input": {"output": "{{ sd.output.images }}"},
            "metadata": {"output": {"title": "output"}},
        }
    )

    recipe = create_recipe(
        [
            start_operator_component,
            instill_model_component_mobilenet_1,
            instill_model_component_mobilenet_2,
            openai_component,
            stability_ai_component,
            end_operator_component,
        ]
    )
    cute_pipeline = Pipeline(client=client, name="cute-pipeline", recipe=recipe)

    cute_pipeline.validate_pipeline()
    Logger.i("cute-pipeline created, validate without error: True")
    i = Struct()
    i.update(
        {
            "input": [
                base64.b64encode(
                    requests.get(
                        "https://artifacts.instill.tech/imgs/dog.jpg",
                        timeout=5,
                    ).content
                ).decode("ascii"),
                base64.b64encode(
                    requests.get(
                        "https://artifacts.instill.tech/imgs/polar-bear.jpg",
                        timeout=5,
                    ).content
                ).decode("ascii"),
            ]
        }
    )

    output = cute_pipeline([i])[0][0]["output"]
    with open("./test.jpg", "wb") as f:
        f.write(base64.b64decode(output))
    assert len(output[0]) != 0
    Logger.i("cute-pipeline triggered, output length not 0: True")
except AssertionError:
    Logger.w("TEST FAILED, ASSERTION MISMATCHED")

Logger.i(
    "==================== Test Done ====================================================================="
)
Logger.i(
    "==================== Cleanup ======================================================================="
)
del csv_pipeline
del instill_model_pipeline
del cute_pipeline
del yolov7
del mobilenet
del instill_connector
del openai_connector
del stability_connector
del csv_connector
