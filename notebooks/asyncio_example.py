import asyncio
import time
import base64
import requests
from google.protobuf.struct_pb2 import Struct

from instill.configuration import global_config
from instill.clients import InstillClient

global_config.set_default(
    url="localhost:8080",
    token="instill_sk_nvGGLp18tM0MpxFxBNsfmNPDz2ICtyKU",
    secure=False,
)

#### we have asyncio support for all rpc calls, especially useful for the heavy IO-bound calls
#### below is a quick showcase of how to utilize both sync and async call, and how their latency look liik


async def trigger_async(inp):
    client = InstillClient(async_enabled=True)
    p_s = client.pipeline_service
    start = time.time()
    resp = await asyncio.gather(
        *[p_s.trigger_pipeline("test", [inp], async_enabled=True) for _ in range(50)]
    )
    print("async: ", time.time() - start)
    client.close()
    await client.async_close()


##### With some selected endpoints from our backend services, mainly pipeline/model triggers, have natively support async call as well, for example


def trigger_native_async(inp):
    client = InstillClient()
    p_s = client.pipeline_service

    start = time.time()
    operations = []
    for _ in range(10):
        operation = p_s.trigger_async_pipeline("test", [inp]).operation
        operations.append(operation)

    for o in operations:
        while not p_s.get_operation(o.name).operation.done:
            time.sleep(0.5)
    print("native async: ", time.time() - start)
    client.close()


def trigger_sync(inp):
    client = InstillClient()
    p_s = client.pipeline_service

    start = time.time()
    for _ in range(50):
        resp = p_s.trigger_pipeline("test", [inp])
    print("sync: ", time.time() - start)
    client.close()


if __name__ == "__main__":
    i = Struct()
    i.update(
        {
            "img": base64.b64encode(
                requests.get(
                    # "https://t3.ftcdn.net/jpg/02/36/99/22/240_F_236992283_sNOxCVQeFLd5pdqaKGh8DRGMZy7P4XKm.jpg",
                    "https://artifacts.instill.tech/imgs/dog.jpg",
                    timeout=5,
                ).content
            ).decode("ascii")
        }
    )
    trigger_sync(i)

    asyncio.run(trigger_async(i))

    trigger_native_async(i)


####### StdOut ########
# sync:  7.4827561378479
# async:  3.0848708152770996
# native async:  1.079378366470337
