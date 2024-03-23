FROM ubuntu:22.04

RUN apt-get update --fix-missing
RUN apt-get install -y \
    python3.11 git make cmake pkg-config xz-utils file binutils gcc texinfo m4 wget autoconf libtool bison flex
RUN apt-get install -y \
    gcc-aarch64-linux-gnu g++-aarch64-linux-gnu binutils-aarch64-linux-gnu
RUN apt-get install -y \
    gcc-powerpc64le-linux-gnu g++-powerpc64le-linux-gnu binutils-powerpc64le-linux-gnu
RUN apt-get install -y \
    gcc-mipsel-linux-gnu g++-mipsel-linux-gnu binutils-mipsel-linux-gnu
RUN apt-get install -y \
    gcc-hppa-linux-gnu g++-hppa-linux-gnu binutils-hppa-linux-gnu
RUN apt-get install -y \
    gcc-s390x-linux-gnu g++-s390x-linux-gnu binutils-s390x-linux-gnu
RUN apt-get install -y \
    gcc-arm-linux-gnueabi g++-arm-linux-gnueabi binutils-arm-linux-gnueabi