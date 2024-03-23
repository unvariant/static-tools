# static gdb

Supports any target that gcc can compile for and glibc supports.


## features
- python support

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