#!/bin/sh

# GUILE OPTIONS
# GUILE_LOAD_COMPILED_PATH="$PWD/guile-files" GUILE_AUTO_COMPILE=0 

LOCPATH="$PWD" PYTHONPATH="$PWD/python-files" LC_ALL="en_US.UTF-8" LANG="en_US.UTF-8" ./gdb --data-directory="$PWD/gdb-files"