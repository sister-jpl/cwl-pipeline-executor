#!/bin/bash

mamba install -c conda-forge -y cwltool
pushd /app
pip install pyopenssl --upgrade
git clone --single-branch --branch sister-dev https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
