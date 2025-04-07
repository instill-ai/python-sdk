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

ARG SDK_VERSION
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \ 
    if [ ! -f instill_sdk-${SDK_VERSION}dev-py3-none-any.whl ]; then \
    pip install --default-timeout=1000 --no-cache-dir instill-sdk==${SDK_VERSION}; \
    else \
    pip install instill_sdk-${SDK_VERSION}dev-py3-none-any.whl; \
    fi

COPY --chown=ray:users model.py _model.py
