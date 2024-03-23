# static gdb

Supports any target that gcc can compile for and glibc supports.

Each bundle in `_packages` contains a single directory with all the files needed to run a static gdb with python.

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