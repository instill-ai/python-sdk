[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/instill-ai/python-sdk/build.yml?branch=main&label=linux)](https://github.com/instill-ai/python-sdk/actions) [![Coverage Status](https://img.shields.io/codecov/c/gh/instill-ai/python-sdk)](https://codecov.io/gh/instill-ai/python-sdk) [![PyPI License](https://img.shields.io/pypi/l/instill-sdk.svg)](https://pypi.org/project/instill-sdk) [![PyPI Version](https://img.shields.io/pypi/v/instill-sdk.svg)](https://pypi.org/project/instill-sdk) [![PyPI Downloads](https://img.shields.io/pypi/dm/instill-sdk.svg?color=orange)](https://pypistats.org/packages/instill-sdk)

> [!IMPORTANT]<br>
> **This SDK tool is under active development**<br>
> For any bug found or featur request, feel free to open any issue regarding this SDK in our [instill-core](https://github.com/instill-ai/instill-core/issues) repo.

# Overview

Welcome to Instill Python SDK, where the world of AI-first application comes alive in the form of Python.

Before you jump into creating your first application with this SDK tool, we recommend you to get familiar with the core concepts of Instill Product first. You can check out our documentation here:

- [Instill Core](https://www.instill.tech/docs/latest/core/concepts)
- [Instill SDK](https://www.instill.tech/docs/latest/sdk/python)

## Setup

> [!NOTE]<br>
> For setting up development environment, please refer to [Contributing](#contributing)

### Requirements

- Python 3.8 - 3.11

### Installation

> [!WARNING]<br>
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

Before we get into this, please make sure a local instance of `Instill VDP` and `Instill Model` is running, and the config file had been populated with the correct `url` and `api_token`

Let's get started!

### Import packages

To Form a pipeine, it required a `start` operator and a `end` operator, we have helper functions to create both

```python
from instill.clients import InstillClient
```

### Get the client

Get the unified client that connect to all the available services offered by `Instill VDP` and `Instill Model`, including

- mgmt_service
- pipeline_service
- model_service
- artifact_service

```python
client = InstillClient()

user = client.mgmt_service.get_user()
# name: "users/admin"
# uid: "4767b74d-640a-4cdf-9c6d-7bb0e36098a0"
# id: "admin"
# ...
# ...
```

Please find more usages for this sdk at [here](https://www.instill.tech/docs/sdk/python#usage)

**You can also find some notebook examples [here](https://github.com/instill-ai/python-sdk/tree/main/notebooks)**

### Create a model

Now create a model `text-generation` in `Instill Model` for later use

```python
import instill.protogen.common.task.v1alpha.task_pb2 as task_interface
model_id = "model_text-generation"
client.model_service.create_model(
    model_id,
    task_interface.Task.TASK_TEXT_GENERATION,
    "REGION_GCP_EUROPE_WEST4",
    "CPU",
    "model-definitions/container",
    {},
)
```

#### Build and deploy the model

`Instill Model` is an advanced MLOps/LLMOps platform that was specifically crafted to facilitate the efficient management and orchestration of model deployments for unstructured data ETL. With `Instill Model`, you can easily create, manage, and deploy your own custom models with ease in `Instill Core` or on the cloud with `Instill Cloud`.

Follow the instructions [here](https://www.instill.tech/docs/model/create) to build and deploy your model.

### Create pipeline

In the section we will be creating a pipeline using this `python-sdk` to harness the power of `Instill VDP`!

The pipeline receipt below is a sample for demo. It simply returns the input string value.

```python
pipeline_id = "pipeline_demo"
client.pipeline_service.create_pipeline(
    pipeline_id,
    "this is a pipeline for demo",
    {
        "output": {"result": {"title": "result", "value": "${variable.input}"}},
        "variable": {"input": {"instillFormat": "string", "title": "input"}},
    },
)
```

#### Validate the pipeline

Before we trigger the pipeline, it is recommended to first validate the pipeline recipe first

```python
# validate the pipeline recipe
client.pipeline_service.validate_pipeline(pipeline_id)
```

#### Trigger the pipeline

Finally the pipeline is done, now let us test it by triggering it!

```python
# we can trigger the pipeline now
client.pipeline_service.trigger_pipeline(pipeline_id, [], [{"input": "hello world"}])
```

And the output should be exactly the same as your input.

## Contributing

Please refer to the [Contributing Guidelines](https://github.com/instill-ai/python-sdk/blob/main/.github/CONTRIBUTING.md) for more details.

## Community support

Please refer to the [community](https://github.com/instill-ai/community) repository.

## License

See the [LICENSE](./LICENSE) file for licensing information.
