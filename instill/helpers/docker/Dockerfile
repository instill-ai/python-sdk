# syntax=docker/dockerfile:1.7-labs

ARG RAY_VERSION=2.47.0
ARG PYTHON_VERSION=-py312
ARG CUDA_VERSION=-cu128

FROM rayproject/ray:${RAY_VERSION}${PYTHON_VERSION}${CUDA_VERSION}

# Install base packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    sudo apt-get update && \
    DEBIAN_FRONTEND=noninteractive sudo apt-get install -y curl vim && \
    sudo rm -rf /var/lib/apt/lists/*

# Install system packages
ARG SYSTEM_PACKAGES
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    sudo apt-get update && \
    for package in ${SYSTEM_PACKAGES}; do \
    DEBIAN_FRONTEND=noninteractive sudo apt-get install -y $package; \
    done && \
    sudo rm -rf /var/lib/apt/lists/*

# Install python packages
ARG PYTHON_PACKAGES
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    for package in ${PYTHON_PACKAGES}; do \
    pip install $package; \
    done

# The python-sdk is a local module that is not installed in the Ray worker environment.
# Ray workers need to deserialize model configurations and deployment settings that were
# created in the runtime environment. These objects may depend on this python-sdk.
# Instead of installing the SDK in the Ray image, we copy
# the entire SDK to /home/ray in development mode (editable or wheel) or
# install the SDK in the Ray image in production mode

COPY --chown=ray:users . .

ARG INSTILL_PYTHON_SDK_PROJECT_NAME
ARG INSTILL_PYTHON_SDK_VERSION
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    if [ ! -z "$INSTILL_PYTHON_SDK_PROJECT_NAME" ]; then \
    pip install -e ${INSTILL_PYTHON_SDK_PROJECT_NAME}; \
    elif [ -f instill_sdk-${INSTILL_PYTHON_SDK_VERSION}dev-py3-none-any.whl ]; then \
    pip install instill_sdk-${INSTILL_PYTHON_SDK_VERSION}dev-py3-none-any.whl; \
    else \
    pip install --default-timeout=1000 instill-sdk==${INSTILL_PYTHON_SDK_VERSION}; \
    fi;

# Set PYTHONPATH to allow dynamic importing for the python-sdk protobuf files
ARG PYTHONPATH_USER_DEFINED_PROTO
ENV PYTHONPATH=${PYTHONPATH_USER_DEFINED_PROTO}