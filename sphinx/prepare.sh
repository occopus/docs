#!/bin/bash

# To compile the documentation, one needs the packages to be installed.
# To prepare compilation do the following:

set -ex

PDIR=env/documentation

rm -rf "$PDIR"

# Create a virtual environment:
virtualenv --no-site-packages "$PDIR"

# Activate it (this step is ALWAYS required before compiling)
source "$PDIR"/bin/activate

pip install --upgrade pip

# Install the locally checked out packages:
pip install --no-deps -r requirements-local.txt --trusted-host pip.lpds.sztaki.hu

set +ex

echo "It's dangerous to go alone. Take these:"
echo "source '$PDIR/bin/activate'"

## Using latest release
##    TBA
