# pylint: disable=no-member,unused-import
import instill.protogen.model.model.v1alpha.model_pb2 as model_interface

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


def test_integration():
    pass
    # mgmt_client, model_client, pipeline_client = clients

    # assert mgmt_client.is_serving()
    # assert model_client.is_serving()
    # assert pipeline_client.is_serving()

    # g_model = GithubModel(
    #     client=model_client,
    #     name=github_model["model_name"],
    #     model_repo=github_model["model_repo"],
    #     model_tag=github_model["model_tag"],
    # )

    # assert g_model.get_state() == model_interface.Model.STATE_OFFLINE

    # g_model.deploy()

    # assert g_model.get_state() == model_interface.Model.STATE_ONLINE
