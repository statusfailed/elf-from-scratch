#!/usr/bin/env bash

./main.py > out.elf
readelf -a out.elf
chmod +x out.elf
./out.elf
