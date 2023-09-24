# Overview

python sdk for Instill AI products

[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/instill-ai/python-sdk/test.yml?branch=main&label=linux)](https://github.com/instill-ai/python-sdk/actions)
[![Coverage Status](https://img.shields.io/codecov/c/gh/instill-ai/python-sdk)](https://codecov.io/gh/instill-ai/python-sdk)
[![PyPI License](https://img.shields.io/pypi/l/instill-sdk.svg)](https://pypi.org/project/instill-sdk)
[![PyPI Version](https://img.shields.io/pypi/v/instill-sdk.svg)](https://pypi.org/project/instill-sdk)
[![PyPI Downloads](https://img.shields.io/pypi/dm/instill-sdk.svg?color=orange)](https://pypistats.org/packages/instill-sdk)

> [!IMPORTANT]  
> **This SDK tool is under heavy development!!**  
> Currently there has yet to be a stable version release, please feel free to open any issue regarding this SDK in our [community](https://github.com/instill-ai/community/issues) repo

## Setup

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

Before we can start using this SDK, you will need to create and fill the host related configs, currently the config file path is `${HOME}/.config/instill/config.yaml`

> [!NOTE]  
> For each instance you are going to config, you will have to obtain an `api_token`, by going to Settings > API Tokens page from the console, no matter it is `Instill Core` or `Instill Cloud`.

Within the config file, you can define multiple instances with the `alias` of your liking, later in the SDK you can refer to this `alias` to switch between the instance.

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

> [!NOTE]  
> You will want to have exactly one instance named `default`. The SDK will attempt to connect to this instance initially, and later on you can swtich to other instances you specified in the config.

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

## Usage

Comming soon


### You can find a [_notebook example_](notebooks/model_usage.ipynb) here

## Contributing

Please refer to the [Contributing Guidelines](./.github/CONTRIBUTING.md) for more details.
