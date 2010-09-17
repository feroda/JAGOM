#!/bin/bash

#TODO: we can do it using python configobj instead of running an external script

if [ -z "$2" ]; then
	echo "Usage $0 <project slug> <admin1> [admin2] [admin3]"
	exit 100
fi

. project_envvars.sh "$1"

shift

# Update members list
sed -i "s/^administrators = .*/administrators = $*/g" $PRJ_AUTH_FILE
