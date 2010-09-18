#!/bin/bash

#TODO: we can do it using python configobj instead of running an external script

if [ -z "$2" ]; then
	echo "Usage $0 <project slug> <admin1> [admin2] [admin3]"
	exit 100
fi

. project_envvars.sh "$1"

shift

VALUE="$1"
shift
for el in $*; do
    VALUE=$VALUE", $el"
done

# Update members list
sed -i "s/^administrators = .*/administrators = $VALUE/g" $PRJ_AUTH_FILE
