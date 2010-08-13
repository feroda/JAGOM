#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage $0 <command>"
	exit 100
fi

PROJECT_ROOT=/var/www/jagom/JAGOM
PINAX_VENV_ROOT=/var/www/jagom/pinax_venv

# NOn funziona perche' non e' in virtualenv e quindi
# non posso importare settings.py
#. $PROJECT_ROOT/bin/base.sh

# activate virtual environment
. $PINAX_VENV_ROOT/bin/activate

cd $PROJECT_ROOT
python manage.py "$1" >> $PROJECT_ROOT/deploy/logs/cron_$1.log 2>&1
