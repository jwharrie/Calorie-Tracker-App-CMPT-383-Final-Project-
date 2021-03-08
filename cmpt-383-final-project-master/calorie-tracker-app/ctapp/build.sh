#!/bin/sh

set -e

swig -python -py3 -modern ctf.i
gcc -fPIC -c ctf.c ctf_wrap.c -I/usr/include/python3.6
ld -shared ctf.o ctf_wrap.o -o _ctf.so
