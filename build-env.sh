#!/bin/bash

mamba install -c conda-forge -y cwltool
pushd /app
pip install pyopenssl --upgrade
git clone https://gitlab.com/geospec/maap-py.git
pushd maap-py
git checkout sister-dev
pip install -e .
