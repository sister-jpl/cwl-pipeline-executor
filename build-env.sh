#!/bin/bash
set -x
basedir=$( cd "$(dirname "$0")" ; pwd -P )

mamba create -n cwl-pipeline -c conda-forge -y cwltool nodejs awscli geopandas=0.12.2 unzip
source activate cwl-pipeline

# Download Coral Mask file
aws s3 cp s3://sister-ops-registry/packages/Coralshapefile20230526123457.zip ${basedir}/workflow/preconditions/Coralshapefile20230526123457.zip
unzip ${basedir}/workflow/preconditions/Coralshapefile20230526123457.zip

pushd /app
# To mitigate AttributeError: module 'importlib_metadata' has no attribute 'MetadataPathFinder'
pip install --upgrade importlib-metadata
git clone --single-branch --branch sister-dev https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
