# pylint: disable=no-member
from instill_sdk.clients.mgmt import MgmtClient
from instill_sdk.clients.model import ModelClient
from instill_sdk.resources.model import GithubModel
import instill_sdk.protogen.model.model.v1alpha.model_pb2 as model_interface
import instill_sdk.protogen.model.model.v1alpha.task_classification_pb2 as classification
from instill_sdk.utils.logger import Logger

local_model = {
    "model_name": "test1",
    "model_description": "test1",
    "model_path": "/Users/heiru/Projects/instill/model-backend/integration-test/data/dummy-cls-model.zip",
}
github_model = {
    "model_name": "test2",
    "model_repo": "instill-ai/model-mobilenetv2-dvc",
    "model_tag": "v1.0-cpu",
}

c = MgmtClient()
if c.is_serving():
    user = c.get_user()
    m = ModelClient(user=user)

    if m.is_serving():
        model = GithubModel(
            client=m,
            name=github_model["model_name"],
            model_repo=github_model["model_repo"],
            model_tag=github_model["model_tag"],
        )

        Logger.i(model.get_state())

        Logger.i(model.deploy())

        Logger.i(model.get_state())

        task_inputs = [
            model_interface.TaskInput(
                classification=classification.ClassificationInput(
                    image_url="https://artifacts.instill.tech/imgs/dog.jpg"
                )
            ),
            model_interface.TaskInput(
                classification=classification.ClassificationInput(
                    image_url="https://artifacts.instill.tech/imgs/tiff-sample.tiff"
                )
            ),
        ]

        Logger.i(model(task_inputs=task_inputs))

        del model
