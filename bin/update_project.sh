#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage $0 <project slug> [name] [description]"
	exit 100
fi

if [ -z "$JAGOM_HOME" ]; then
    echo "Error: JAGOM_HOME is not set, cannot continue"
    exit 101
fi

function settings_var {
  export name=$1
  (cd $JAGOM_HOME; (echo "from settings import $name"; echo "print $name" ) |python )
}

PRJ="$1"
if [ ! -z "$2" ]; then
    NAME="$2"
    if [ ! -z "$3" ]; then
        DESCRIPTION="$3"
    fi
fi

PRJS_ENVS_PATH=$(settings_var PRJS_ENVS_PATH )
PRJ_LINT_PATH=$(settings_var PRJ_LINT_PATH )
PRJ_ROOT="$PRJ_ENVS_PATH/$PRJ"
PRJ_ROOT_CONF_FILE=$PRJ_ROOT/conf/trac.ini

if [ ! -d "$PRJS_ENVS_PATH" ]; then
    echo "Error: directory $PRJS_ENVS_PATH does not exist"
    exit 102
fi

# Update name and description if present
if [ "$NAME" ]; then
    sed -i "s/^name\ =.*/name = $NAME/g" $PRJ_ROOT_CONF_FILE
    if [ "$DESCRIPTION" ]; then
        sed -i "s/^descr\ =.*/descr = $DESCRIPTION/g" $PRJ_ROOT_CONF_FILE
    fi
fi

chmod -R u+w $PRJ_ROOT

for f in VERSION README; do
	chmod u-w $PRJ_ROOT/$f
done

