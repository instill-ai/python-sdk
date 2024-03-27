ARG RAY_VERSION
ARG PYTHON_VERSION
ARG CUDA_SUFFIX

FROM rayproject/ray:${RAY_VERSION}-py${PYTHON_VERSION}${CUDA_SUFFIX}-aarch64 as base-arm64
FROM rayproject/ray:${RAY_VERSION}-py${PYTHON_VERSION}${CUDA_SUFFIX} as base-amd64

FROM base-${TARGETARCH}

RUN sudo apt-get update && sudo apt-get install curl -y

ARG PACKAGES
RUN for package in ${PACKAGES}; do \
    pip install --default-timeout=1000 --no-cache-dir $package; \
    done;

WORKDIR /home/ray
COPY . .
