#!/bin/bash

set -ex

for f in ../tutorials/*; do
    if [ -d "$f" ]; then
        tar -cvf "$f".tar.gz "$f"
    fi
done
