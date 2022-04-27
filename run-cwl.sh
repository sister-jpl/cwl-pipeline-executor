#!/bin/bash

source activate cwl-pipeline

basedir=$( cd "$(dirname "$0")" ; pwd -P )

python ${basedir}/run_cwl_workflow.py

