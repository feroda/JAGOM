#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage $0 <project slug> <admin username> [name] [description] [base project path]"
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
    ADMIN="$2"
else
    echo "Error: you MUST specify admin username"
    exit 102
fi

if [ ! -z "$3" ]; then
    NAME="$3"
    if [ ! -z "$4" ]; then
        DESCRIPTION="$4"
    fi
fi

PRJ_ENV_ROOT=$(settings_var PRJ_ENV_ROOT )
PRJS_ENVS_PATH=$(settings_var PRJS_ENVS_PATH )
PRJ_LINT_PATH=${4:-$(settings_var PRJ_LINT_PATH )}
PRJ_ROOT="$PRJS_ENVS_PATH/$PRJ"
PRJ_ROOT_CONF_FILE=$PRJ_ROOT/conf/trac.ini
PRJ_ROOT_AUTH_FILE=$PRJ_ROOT/conf/authzpolicy.conf

if [ ! -d "$PRJS_ENVS_PATH" ]; then
    echo "Error: directory $PRJS_ENVS_PATH does not exist"
    exit 102
fi

if [ -d "$PRJ_ROOT" ]; then
    #Project already exists
    exit 1
fi

cp -a $PRJ_LINT_PATH $PRJ_ROOT

# Update name and description if present
if [ "$NAME" ]; then
    sed -i "s/^name\ =.*/name = $NAME/g" $PRJ_ROOT_CONF_FILE
    if [ "$DESCRIPTION" ]; then
        sed -i "s/^descr\ =.*/descr = $DESCRIPTION/g" $PRJ_ROOT_CONF_FILE
    fi
fi

# Update administrators list
sed -i "s/^administrators = .*/administrators = $ADMIN/g" $PRJ_ROOT_AUTH_FILE

chmod -R u+w $PRJ_ROOT

for f in VERSION README; do
	chmod u-w $PRJ_ROOT/$f
done

# Activate projects virtualenv and perform trac-admin upgrade
cd $PRJ_ENV_ROOT
. bin/activate
trac-admin $PRJ_ROOT upgrade
trac-admin $PRJ_ROOT permission add $ADMIN TRAC_ADMIN

# TODO FIXME: we should also
# remove all wiki/Private* pages
# remove all tickets comments

