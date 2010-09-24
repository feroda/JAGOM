#!/bin/bash

if [ -z "$2" ]; then
	echo "Usage $0 <project slug> <admin username> [name] [description] [base project path]"
	exit 100
fi

. project_envvars.sh "$1"

ADMIN="$2"

if [ ! -z "$3" ]; then
    NAME="$3"
    if [ ! -z "$4" ]; then
        DESCRIPTION="$4"
    fi
fi

if [ ! -d "$PRJS_ENVS_PATH" ]; then
    echo "Error: directory $PRJS_ENVS_PATH does not exist"
    exit 102
fi

if [ -d "$PRJ_ROOT" ]; then
    #Project already exists
    exit 1
fi

PRJ_LINT_PATH=${5:-$(settings_var PRJ_LINT_PATH )}

#Copy dereferencing symlinks
cp -rL $PRJ_LINT_PATH $PRJ_ROOT

# Update name and description if present
if [ "$NAME" ]; then
    sed -i "s/^name\ =.*/name = $NAME/g" $PRJ_CONF_FILE
    if [ "$DESCRIPTION" ]; then
        sed -i "s/^descr\ =.*/descr = $DESCRIPTION/g" $PRJ_CONF_FILE
    fi
fi
# Update base_url
sed -i "s@^base_url\ = \(.*/\).*@base_url = \1$1@g" $PRJ_CONF_FILE

# Update administrators list
sed -i "s/^administrators = .*/administrators = $ADMIN/g" $PRJ_AUTH_FILE
# TODO: In 0.1 all members are administrators
# sed -i "s/^members = .*/members = /g" $PRJ_AUTH_FILE

chmod -R u+w $PRJ_ROOT

for f in VERSION README; do
	chmod u-w $PRJ_ROOT/$f
done

# Activate projects virtualenv and perform trac-admin upgrade
cd $PRJ_ENV_ROOT
. bin/activate
trac-admin $PRJ_ROOT upgrade

# remove all wiki/Private* pages

# TODO FIXME: should we also reset the project ???
# remove all tickets comments
# remove all "completed milestone"

