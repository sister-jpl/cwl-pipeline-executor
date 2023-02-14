#!/bin/bash

mamba install -c conda-forge -y cwltool
pushd /app
pip install pyopenssl --upgrade
git clone https://gitlab.com/geospec/maap-py.git
pushd maap-py
git checkout 2.0
pip install -e .
