# syntax=docker/dockerfile:1.7-labs
ARG RAY_VERSION
ARG PYTHON_VERSION
ARG CUDA_SUFFIX
ARG TARGET_ARCH_SUFFIX

FROM rayproject/ray:${RAY_VERSION}-py${PYTHON_VERSION}${CUDA_SUFFIX}${TARGET_ARCH_SUFFIX}

RUN sudo apt-get update && sudo apt-get install curl -y

ARG SYSTEM_PACKAGES
RUN for package in ${SYSTEM_PACKAGES}; do \
    sudo apt-get install $package; \
    done;

ARG PACKAGES
RUN for package in ${PACKAGES}; do \
    pip install --default-timeout=1000 --no-cache-dir $package; \
    done;

COPY --chown=ray:users --exclude=model.py . .

ARG SDK_VERSION
RUN if [ ! -f instill_sdk-${SDK_VERSION}dev-py3-none-any.whl ]; then \
        pip install --default-timeout=1000 --no-cache-dir instill-sdk==${SDK_VERSION}; \
    else \
        pip install instill_sdk-${SDK_VERSION}dev-py3-none-any.whl; \
    fi;

WORKDIR /home/ray
COPY --chown=ray:users model.py _model.py
