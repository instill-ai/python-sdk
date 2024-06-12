# pylint: disable=no-member,no-name-in-module
# import base64
# import requests
import pprint
from instill.configuration import global_config

from google.protobuf.struct_pb2 import Struct
from instill.resources import Pipeline
from instill.clients import get_client
from instill.utils.logger import Logger

global_config.set_default(
    url="localhost:8080",
    token="instill_sk_rFMhSpG3EvMuQtYBkBzHmuT74pAjNDsf",
    secure=False,
)

try:
    client = get_client()

    Logger.i(
        "==================== mgmt =========================================================================="
    )
    assert client.mgmt_service.is_serving()
    Logger.i("mgmt client created, assert status == serving: True")

    user = client.mgmt_service.get_user().user
    assert user.id == "admin"
    Logger.i("mgmt get user, assert default user id == admin: True")

    Logger.i(
        "==================== model ========================================================================="
    )
    assert client.model_service.is_serving()
    Logger.i("model client created, assert status == serving: True")

    Logger.i(
        "==================== pipeline ======================================================================"
    )

    assert client.pipeline_service.is_serving()
    Logger.i("pipeline client created, assert status == serving: True")

    pipeline = Pipeline(client=client, name="stomata-detection")
    assert pipeline.resource != None
    Logger.i("pipeline created, assert pipeline != None: True")
    pprint.pprint(pipeline.get_recipe())
    inp = Struct()
    inp.update(
        {
            "i": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        }
    )
    pprint.pprint(pipeline([inp], silent=False))

except AssertionError:
    Logger.w("TEST FAILED, ASSERTION MISMATCHED")
except Exception as e:
    Logger.w(f"TEST FAILED, ERROR:{e}")

Logger.i(
    "==================== Test Done ====================================================================="
)
