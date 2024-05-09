[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/instill-ai/python-sdk/build.yml?branch=main&label=linux)](https://github.com/instill-ai/python-sdk/actions)
[![Coverage Status](https://img.shields.io/codecov/c/gh/instill-ai/python-sdk)](https://codecov.io/gh/instill-ai/python-sdk)
[![PyPI License](https://img.shields.io/pypi/l/instill-sdk.svg)](https://pypi.org/project/instill-sdk)
[![PyPI Version](https://img.shields.io/pypi/v/instill-sdk.svg)](https://pypi.org/project/instill-sdk)
[![PyPI Downloads](https://img.shields.io/pypi/dm/instill-sdk.svg?color=orange)](https://pypistats.org/packages/instill-sdk)

> [!IMPORTANT]  
> **This SDK tool is under active development**  
> For any bug found or featur request, feel free to open any issue regarding this SDK in our [community](https://github.com/instill-ai/community/issues) repo.

# Overview

Welcome to Instill Python SDK, where the world of AI-first application comes alive in the form of Python.

Before you jump into creating your first application with this SDK tool, we recommend you to get familiar with the core concepts of Instill Product first. You can check out our documentation here:

- [Instill Core](https://www.instill.tech/docs/latest/core/concepts)
- [Instill SDK](https://www.instill.tech/docs/latest/sdk/python)

## Setup

> [!NOTE]  
> For setting up development environment, please refer to [Contributing](#contributing)

### Requirements

- Python 3.8+

### Installation

> [!WARNING]  
> If your host machine is on arm64 architecture(including Apple silicon machines, equipped with m1/m2 processors), there are some issues when installing `grpcio` within `conda` environment. You will have to manually build and install it like below. Read more about this issue [here](https://github.com/grpc/grpc/issues/33714).

```bash
$ GRPC_PYTHON_LDFLAGS=" -framework CoreFoundation" pip install grpcio --no-binary :all:
```

Install it directly into an activated virtual environment:

```text
$ pip install instill-sdk
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add instill-sdk
```

### Check import

After installation, you can check if it has been installed correctly:

```text
$ python
>>> import instill
>>> instill.__version__
```

### Config `Instill Core` or `Instill Cloud` instance

Before we can start using this SDK, you will need to properly config your target instance. We support two ways to setup the configs, which are

#### Config file

create a config file under this path `${HOME}/.config/instill/sdk/python/config.yml`, and within that path you will need to fill in some basic parameters for your desired host.[^1]

[^1]: You can obtain an `api_token` by simply going to Settings > API Tokens page from the console, no matter it is `Instill Core` or `Instill Cloud`.

Within the config file, you can define multiple instances with the `alias` of your liking, later in the SDK you can refer to this `alias` to switch between instances.[^2]

[^2]: SDK is default to look for instance named `default` first, and will fall back to the first instance entry in the config file if `default` not found

```yaml
hosts:
  alias1:
    url:    str
    secure: bool
    token:  str
  alias2:
    url:    str
    secure: bool
    token:  str
  ...
  ...
```

Example:

```yaml
hosts:
  default:
    url: localhost:8080
    secure: false
    token: instill_sk***
  cloud:
    url: api.instill.tech
    secure: true
    token: instill_sk***
```

#### At runtime

If you do not like the idea of having to create a config file, you can also setup your target instance by doing the following at the very beginning of your script.

```python
from instill.configuration import global_config

global_config.set_default(
    url="api.instill.tech",
    token="instill_sk***",
    secure=True,
)
```

## Usage

### Create client

**You can also find some notebook examples [here](https://github.com/instill-ai/python-sdk/tree/main/notebooks)**

Simply import the `get_client` function to get the client that are connected to all services with the config you setup previously.

```python
from instill.clients import get_client

client = get_client()
```

> [!NOTE]  
> Remember to call `client.close()` at the end of script to release the channel and the underlying resources

If you have not set up `Instill VDP` or `Instill Model`, you will get a warning like this:

```bash
2023-09-27 18:49:04,871.871 WARNING  Instill VDP is not serving, VDP functionalities will not work
2023-09-27 18:49:04,907.907 WARNING  Instill Model is not serving, Model functionalities will not work
```

You can check the readiness of each service:

```python
client.mgmt_service.is_serving()
# True
client.pipeline_service.is_serving()
# True
client.model_service.is_serving()
# True
```

You can also switch to other instances

```python
client.set_instance("your-instance-in-config")
client.mgmt_service.instance
# 'your-instance-in-config'
```

After making sure all desired services are serving, we can check the user status by:

```python
client.mgmt_service.get_user()
```

If you have a valid `api_token` in your config file, you should see something like this:

```
name: "users/admin"
uid: "4767b74d-640a-4cdf-9c6d-7bb0e36098a0"
id: "admin"
type: OWNER_TYPE_USER
create_time {
  seconds: 1695589596
  nanos: 36522000
}
update_time {
  seconds: 1695589749
  nanos: 544980000
}
email: "hello@instill.tech"
first_name: "Instill"
last_name: "AI"
org_name: "Instill AI"
role: "hobbyist"
newsletter_subscription: true
cookie_token: ""
```

#### Now we can proceed to create resources

### Create Model

Let's say we want to serve a `yolov7` model from `github` with the following configs

```python
model_name = "yolov7"
model_repo = "instill-ai/model-yolov7-dvc"
model_tag = "v1.0-cpu"
```

Simply import the GithubModel resource and fill in the corresponding fields

```python
from instill.resources.model import GithubModel

yolov7 = GithubModel(
  client=client,
  name=model_name,
  model_repo=model_repo,
  model_tag=model_tag,
)
```

After the creation is done, we can check the state of the model[^3]

[^3]: [State definition](https://www.instill.tech/docs/model/core-concepts/overview#state)

```python
yolov7.get_state()
# 1
# means STATE_OFFLINE
```

Now we can deploy the model

```python
yolov7.deploy()
```

Check the status

```python
yolov7.get_state()
# 2
# means STATE_ONLINE
```

Trigger the model with the correct `task` type[^4]

[^4]: Check out our [task protocol](https://www.instill.tech/docs/model/core-concepts/ai-task) to learn more, or read our [json schema](https://raw.githubusercontent.com/instill-ai/connector-ai/main/pkg/instill/config/seed/data.json) directly

```python
from instill.resources import model_pb, task_detection
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
```

Now if you `print` the outputs, you will get a list of specific `task` output, in this case is a list of `TASK_DETECTION` output

```
[detection {
  objects {
    category: "dog"
    score: 0.958271801
    bounding_box {
      top: 102
      left: 324
      width: 208
      height: 403
    }
  }
  objects {
    category: "dog"
    score: 0.945684791
    bounding_box {
      top: 198
      left: 130
      width: 198
      height: 236
    }
  }
}
, detection {
  objects {
    category: "bear"
    score: 0.968335629
    bounding_box {
      top: 85
      left: 291
      width: 554
      height: 756
    }
  }
}
, detection {
  objects {
    category: "bear"
    score: 0.948612273
    bounding_box {
      top: 458
      left: 1373
      width: 1298
      height: 2162
    }
  }
}
]
```

### Create connector

With similiar conecpt as creating `model`, below is the steps to create a `instill model connector`

First import our predefined `InstillModelConnector` and config dataclass `InstillModelConnector2`[^5]

[^5]: config dataclass is auto-gen from our json schema, we will refacor the source json to make the dataclass name makes more sense

```python
from instill.resources.schema.instill import InstillModelConnector1
from instill.resources import InstillModelConnector, connector_pb, const
```

Then we set up the connector resource information[^6]

[^6]: Find out the resource definition in our [json schema](https://raw.githubusercontent.com/instill-ai/connector-ai/8bf4463b57a5b668f3f656e4c168561b623d065d/pkg/instill/config/seed/resource.json)

```python
# create the config dataclass object and fill in necessary fields
instill_model_config = InstillModelConnector1(mode=const.INSTILL_MODEL_INTERNAL_MODE)

instill_model = InstillModelConnector(
    client,
    name="instill",
    config=instill_model_config,
)
```

After the connector is created, the state should be `STATE_DISCONNECTED`

```python
instill_model.get_state() == connector_pb.Connector.STATE_DISCONNECTED
# True
```

Now we can test the connection for the newly configured connector, to make sure the connection with the host can be established

```python
instill_model.test() == connector_pb.Connector.STATE_CONNECTED
# True
```

### Create pipeline

Since we have created a `Instill Model Connector` that connect to our `Instill Model` instance, we can now create a pipeline that utilize both `Instill VDP` and `Instill Model`

First we import `Pipeline` class and other helper functions

```python
from instill.resources.schema import (
  instill_task_detection_input,
  start_task_start_metadata,
  end_task_end_metadata,
)
from instill.resources import (
  const,
  InstillModelConnector,
  Pipeline,
  create_start_operator,
  create_end_operator,
  create_recipe,
  populate_default_value,
)
```

To Form a pipeine, it required a `start` operator and a `end` operator, we have helper functions to create both

```python
# define start operator input spec
start_metadata = {}
start_metadata.update(
  {
    "input_image": start_task_start_metadata.Model1(
        instillFormat="image/*",
        title="Image",
        type="string",
    )
  }
)
# create start operator
start_operator_component = create_start_operator(start_metadata)
```

If you wish to define multiple input fields in the start operator, simply add more `"key"` and `"start_task_start_metadata.Model1"` pair by

```python
start_metadata.update(
  {
    "input_image": start_task_start_metadata.Model1(
        instillFormat="{your input format}",
        title="{input title}",
        type="{input type}",
    )
  }
)
```

Now we can create a `model` `component`. From the already defined `instill Model Connector`, we can utilize the models served on `Instill Model`, import them as a `component`.

```python
# first we create the input for the component from the dataclass
# here we need to specify which model we want to use on our `Instill Model` instance
# in this case there is only one model we deployed, which is the yolov7 model
instill_model_input = instill_task_detection_input.Input(
  model_namespace="admin",
  model_id="yolov7",
  image_base64="{start.input_image}",
)
# create model connector component from the connector resource we had created previously
instill_model_connector_component = instill_model.create_component(
  name="yolov7",
  inp=instill_model_input,
)

# define end operator input and metadata spec
end_operator_inp = {}
end_operator_inp.update({"inference_result": "{yolov7.output.objects}"})
end_operator_metadata = {}
end_operator_metadata.update(
  {"inference_result": end_task_end_metadata.Model1(title="result")}
)
# create end operator
end_operator_component = create_end_operator(end_operator_inp, end_operator_metadata)
```

We now have all the components ready for the pipeline. Next, we add them into the recipe and create a pipeline.

```python
# create a recipe to construct the pipeline
recipe = create_recipe([start_operator_component, instill_model_connector_component, end_operator_component])
# create pipeline
instill_model_pipeline = Pipeline(
  client=client, name="instill-model-pipeline", recipe=recipe
)
```

Finally the pipeline is done, now let us test it by triggering it!

```python
# we can trigger the pipeline now
import base64
import requests
from google.protobuf.struct_pb2 import Struct
i = Struct()
i.update(
  {
    "input_image": base64.b64encode(
      requests.get(
        "https://artifacts.instill.tech/imgs/dog.jpg", timeout=5
      ).content
    ).decode("ascii")
  }
)
# verify the output
instill_model_pipeline([i])[0][0]["inference_result"][0]["category"] == "dog"
```

## Contributing

Please refer to the [Contributing Guidelines](https://github.com/instill-ai/python-sdk/blob/main/.github/CONTRIBUTING.md) for more details.

## Community support

Please refer to the [community](https://github.com/instill-ai/community) repository.

## License

See the [LICENSE](./LICENSE) file for licensing information.
