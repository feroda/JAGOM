#!/bin/bash

if [ -z "$JAGOM_HOME" ]; then
    echo "Error: JAGOM_HOME is not set, cannot continue"
    exit 101
fi

. base_envvars.sh

# Activate projects virtualenv 
cd $PRJ_ENV_ROOT
. bin/activate

for PRJ in `ls $PRJS_ENVS_PATH`; do

    PRJ_ROOT="$PRJS_ENVS_PATH/$PRJ"

    # Perform trac-admin upgrade
    trac-admin $PRJ_ROOT upgrade

done
