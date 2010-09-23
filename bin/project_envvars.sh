#!/bin/bash

# Common variables for project environments

if [ -z "$JAGOM_HOME" ]; then
    echo "Error: JAGOM_HOME is not set, cannot continue"
    exit 101
fi

. base_envvars.sh

PRJ="$1"
PRJ_ROOT="$PRJS_ENVS_PATH/$PRJ"
PRJ_CONF_FILE=$PRJ_ROOT/conf/trac.ini
PRJ_AUTH_FILE=$PRJ_ROOT/conf/authzpolicy.conf

