#!/bin/bash

mamba create -n cwl-pipeline -c conda-forge -y cwltool

pushd /
rm -rf maap-py
git clone --single-branch system-test-8 https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
