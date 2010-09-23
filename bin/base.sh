
# AAA: OBSOLETED ! !! ! 
exit 0

if [ -z "$JAGOM_HOME" ]; then
    echo "Error: JAGOM_HOME is not set, cannot continue"
    exit 101
fi

function settings_var {
  export name=$1
  (cd $JAGOM_HOME; (echo "from settings import $name"; echo "print $name" ) |python )
}

export PINAX_VENV_ROOT=$(settings_var PINAX_VENV_ROOT)
export PROJECT_ROOT=$JAGOM_HOME

PRJS_ENVS_PATH=$(settings_var PRJS_ENVS_PATH )
PRJ_LINT_PATH=$(settings_var PRJ_LINT_PATH )
PRJ_ROOT="$PRJS_ENVS_PATH/$PRJ"
PRJ_ROOT_CONF_FILE=$PRJ_ROOT/conf/trac.ini


