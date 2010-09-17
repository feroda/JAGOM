#!/bin/bash

#TODO: we can do it using python configobj instead of running an external script

if [ -z "$2" ]; then
	echo "Usage $0 <project slug> <member1> [member2] [member3]"
	exit 100
fi

. project_envvars.sh "$1"

shift

# Update members list
sed -i "s/^members = .*/members = $*/g" $PRJ_AUTH_FILE
