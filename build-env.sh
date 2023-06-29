#!/bin/bash
set -x
mamba create -n cwl-pipeline -c conda-forge -y cwltool nodejs awscli
source activate cwl-pipeline
pushd /app
# Download Coral Mask file
aws s3 cp s3://sister-ops-registry/packages/Coralshapefile20230526123457.zip .
unzip Coralshapefile20230526123457.zip

# To mitigate AttributeError: module 'importlib_metadata' has no attribute 'MetadataPathFinder'
pip install --upgrade importlib-metadata
git clone --single-branch --branch sister-dev https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
