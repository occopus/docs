#!/bin/bash

set -ex

for f in ../tutorials/*; do
    if [ -d "$f" ]; then
        tar -czvf "$f".tar.gz "$f"
    fi
done
