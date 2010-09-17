#!/bin/bash

# Common variables for project environments

if [ -z "$JAGOM_HOME" ]; then
    echo "Error: JAGOM_HOME is not set, cannot continue"
    exit 101
fi

function settings_var {
  export name=$1
  (cd $JAGOM_HOME; (echo "from settings import $name"; echo "print $name" ) |python )
}

PRJ="$1"
PRJ_ENV_ROOT=$(settings_var PRJ_ENV_ROOT )
PRJS_ENVS_PATH=$(settings_var PRJS_ENVS_PATH )
PRJ_ROOT="$PRJS_ENVS_PATH/$PRJ"
PRJ_CONF_FILE=$PRJ_ROOT/conf/trac.ini
PRJ_AUTH_FILE=$PRJ_ROOT/conf/authzpolicy.conf

