# Overview

python sdk for Instill AI products

[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/instill-ai/python-sdk/test.yml?branch=main&label=linux)](https://github.com/instill-ai/python-sdk/actions)
[![Coverage Status](https://img.shields.io/codecov/c/gh/instill-ai/python-sdk)](https://codecov.io/gh/instill-ai/python-sdk)
[![PyPI License](https://img.shields.io/pypi/l/instill-python-sdk.svg)](https://pypi.org/project/instill-python-sdk)
[![PyPI Version](https://img.shields.io/pypi/v/instill-python-sdk.svg)](https://pypi.org/project/instill-python-sdk)
[![PyPI Downloads](https://img.shields.io/pypi/dm/instill-python-sdk.svg?color=orange)](https://pypistats.org/packages/instill-python-sdk)

> :exclamation: **This SDK tool is under heavy development!!**  
> Currently there is no official wheel on `pypi`, and documentation on how to setup and tutorials will be available soon.Stay tuned!  
> For now, you can refer to the `Contributing Guidelines` to setup a development environment

## Setup

### Requirements

- Python 3.8+

### Installation

Install it directly into an activated virtual environment:

```text
$ pip install instill-sdk
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add instill-sdk
```

## Usage

After installation, the package can be imported:

```text
$ python
>>> import instill_sdk
>>> instill_sdk.__version__
```

### You can find a [_notebook example_](notebooks/model_usage.ipynb) here

## Contributing

Please refer to the [Contributing Guidelines](./.github/CONTRIBUTING.md) for more details.
