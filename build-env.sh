#!/bin/bash

mamba install -c conda-forge -y cwltool
pushd /app
git clone --single-branch system-test-8 https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
