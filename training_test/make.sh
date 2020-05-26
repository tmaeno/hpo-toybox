#!/usr/bin/env bash

tar cvfz calo_dnn_training.tgz training.sh exec_in_container.sh make_input.py
scp calo_dnn_training.tgz atlpan@aipanda048:/var/panda/cache/pandaserver/