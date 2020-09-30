#!/bin/bash

set -ex

PWD=`pwd`

cd ../tutorials
tar -czvf "$1".tar.gz "$1"

# for f in ./*; do
#     if [ -d "$f" ]; then
#         tar -czvf "$f".tar.gz "$f"
#     fi
# done

cd $PWD
