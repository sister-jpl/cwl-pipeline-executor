#!/bin/bash

mamba install -c conda-forge -y cwltool
pushd /app
git clone https://gitlab.com/geospec/maap-py.git
pushd maap-py
git checkout system-test-8
pip install -e .
