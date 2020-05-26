#!/usr/bin/env bash

export CURRENT_DIR=$PWD
export CALO_DNN_DIR=/ATLASMLHPO/payload/CaloImageDNN
export PYTHONPATH=$CALO_DNN_DIR/deepcalo

cd $CALO_DNN_DIR
curl -sSL https://cernbox.cern.ch/index.php/s/HfHYEsmJNWiefu3/download | tar -xzvf -;
cp $CURRENT_DIR/input.json $CALO_DNN_DIR/exp_scalars
source $CALO_DNN_DIR/run.sh
cp $CALO_DNN_DIR/exp_scalars/output.json $CURRENT_DIR
tar cvfz $CURRENT_DIR/metrics.tgz mlruns/*
