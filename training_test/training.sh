#!/usr/bin/env bash

# wrapper for https://gitlab.cern.ch/zhangruihpc/payload#2-caloimagednn

singularity build __image docker://gitlab-registry.cern.ch/zhangruihpc/endpointcontainer:mlflow
singularity exec -w -H $PWD:/home __image bash exec_in_container.sh
