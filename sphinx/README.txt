#!/bin/bash

# To compile the documentation, one needs the packages to be installed.
# To prepare compilation do the following:

# Create a virtual environment:
virtualenv env/documentation

# Activate it (this step is ALWAYS required before compiling)
source env/documentation/bin/activate

## Using bleeding-edge code

# Clone all repositories next to this repository:
REPOS='compiler enactor info-broker infrastructure-processor cloud-handler util'
for i in $REPOS; do
    git clone git@gitlab.lpds.sztaki.hu:cloud-orchestrator/$i.git ../../$i
done

# Install the locally checked out packages:

pip install --no-deps -r requirements-local.txt --trusted-host pip.lpds.sztaki.hu

## Using latest release
##    TBA
