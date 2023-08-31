import pprint
from instill_sdk import client

c = client.MgmtClient()

if c.is_serving():
    user = c.get_user()
    m = client.ModelClient(user=user)

    if m.is_serving():
        pprint.pprint(
            m.create_model_local(
                model_name="test1",
                model_description="test1",
                model_path="/Users/heiru/Projects/instill/model-backend/integration-test/data/dummy-cls-model.zip",
            )
        )

        pprint.pprint(
            m.create_github_model(
                model_name="test2",
                model_repo="instill-ai/model-mobilenetv2-dvc",
                model_tag="v1.0-cpu",
            )
        )

        pprint.pprint(m.deploy_model(model_name="test2"))

        for name in ["test1", "test2"]:
            pprint.pprint(m.delete_model(model_name=name))
