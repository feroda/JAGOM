#!/bin/bash 

if [ -f "$1" ]; then
    strfile -r "$1"
else
    echo "Usage: $0 <quote file>"
    exit 100
fi
