# syntax=docker/dockerfile:1.7-labs
ARG RAY_VERSION
ARG PYTHON_VERSION
ARG CUDA_SUFFIX
ARG TARGET_ARCH_SUFFIX

FROM rayproject/ray:${RAY_VERSION}-py${PYTHON_VERSION}${CUDA_SUFFIX}${TARGET_ARCH_SUFFIX}

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    sudo apt-get update && \
    DEBIAN_FRONTEND=noninteractive sudo apt-get install -y tzdata curl vim && \
    sudo rm -rf /var/lib/apt/lists/*

ARG SYSTEM_PACKAGES
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    sudo apt-get update && \
    for package in ${SYSTEM_PACKAGES}; do \
    DEBIAN_FRONTEND=noninteractive sudo apt-get install -y $package; \
    done && \
    sudo rm -rf /var/lib/apt/lists/*

ARG PYTHON_PACKAGES
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    for package in ${PYTHON_PACKAGES}; do \
    pip install --default-timeout=1000 $package; \
    done

COPY --chown=ray:users --exclude=model.py . .

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

COPY --chown=ray:users model.py _model.py
