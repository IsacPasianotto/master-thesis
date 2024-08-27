FROM pasianeight/openmpi-builder:deb12 as builder

RUN mkdir -p /osu

COPY --from=pasianeight/osu-code-provider:latest /code/osu-micro-benchmarks-7.4 /osu

WORKDIR /osu

RUN ./configure CC=mpicc CXX=mpicxx --prefix=/usr/local/osu \
    && make \
    && make install

FROM pasianeight/mpi-operator:deb12 as operator

COPY --from=builder /usr/local/osu /home/mpiuser/osu
