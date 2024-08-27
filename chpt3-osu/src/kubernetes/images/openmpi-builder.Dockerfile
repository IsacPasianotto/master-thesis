FROM debian:12 as builder

RUN apt update \
    && apt install -y --no-install-recommends \
        g++ \
        libopenmpi-dev \
        make \
    && rm -rf /var/lib/apt/lists/*
