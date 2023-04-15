#!/bin/bash
set -x
mamba install -c conda-forge -y cwltool
pushd /app
git clone --single-branch --branch sister-dev https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
