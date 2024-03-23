# static gdb
Supports any target that gcc can compile for and glibc supports.

Each bundle in `_packages` contains a single directory with all the files needed to run a static gdb with python.

## building
To compile for a custom target change the `host` field in `config.json` to the proper target and install the `gcc`, `g++`, and `binutils` cross compiler tools for that proper arch in `_docker/Dockerfile`.

in the repo root:
```console
cd _docker
docker build . -t static
cd ..
docker run --rm -w /static -v "$PWD":/static -it static /bin/bash
```

once in docker:
```console
python3.11 main.py binutils-gdb
```

Any build failures for gdb specifically will be located in `binutils-gdb/_build/_build.log`.

Any `configure` failures will emit a `config.log` in whatever packages source directory, or in that packages respective `_build` directory for an out of tree build.

In order to restart a build for a specific package delete the `_build` directory inside that package, NOT the toplevel repo `_build` directory.
If that package does not support out of tree building `make distclean` usually works and if all else fails delete the entire package source and redownload.

## features
- python support
    - can run [gef](https://github.com/bata24/gef)

## disabled features
- debuginfod
    - requires either curl or microhttp
- guile
    - annoying and doesn't seem to do much
- tui
    - requires ncurses
- source-highlight
    - gdb can't seem to detect this properly

## tested architectures
- arm-linux-gnueabi
- aarch64-linux-gnu
- alpha-linux-gnu
- mipsel-linux-gnu
- powerpc64le-linux-gnu
- s390x-linux-gnu

## known failing architectures
- hppa
    - python miscompiles

## TODO
- try musl maybe?
- package other tools
    - strace
    - readelf
    - elfutils