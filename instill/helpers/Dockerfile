ARG RAY_VERSION
ARG PYTHON_VERSION
ARG CUDA_SUFFIX
ARG TARGET_ARCH_SUFFIX

FROM rayproject/ray:${RAY_VERSION}-py${PYTHON_VERSION}${CUDA_SUFFIX}${TARGET_ARCH_SUFFIX}

ARG PACKAGES

RUN sudo apt-get update && sudo apt-get install curl -y

RUN for package in ${PACKAGES}; do \
    pip install --default-timeout=1000 --no-cache-dir $package; \
    done;

WORKDIR /home/ray
COPY . .
