#!/bin/bash
set -x
mamba install -c conda-forge -y cwltool
pushd /app
# To mitigate AttributeError: module 'importlib_metadata' has no attribute 'MetadataPathFinder'
pip install --upgrade importlib-metadata
git clone --single-branch --branch sister-dev https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
