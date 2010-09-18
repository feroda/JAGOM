#!/bin/bash

#TODO: we can do it using python configobj instead of running an external script

if [ -z "$2" ]; then
	echo "Usage $0 <project slug> <member1> [member2] [member3]"
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
sed -i "s/^members = .*/members = $VALUE/g" $PRJ_AUTH_FILE
