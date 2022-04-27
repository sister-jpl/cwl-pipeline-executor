#!/bin/bash

# source activate cwl-pipeline
set -x

basedir=$( cd "$(dirname "$0")" ; pwd -P )
python ${basedir}/create_workflow_inputs.py $1
WORKFLOW_INPUTS=$(ls $PWD/workflow-inputs.yml)

# pushd is important for the ymls to find the python file doing a $PWD
pushd ${basedir}/workflow
cwltool prisma-workflow.cwl.yml ${WORKFLOW_INPUTS}
popd
