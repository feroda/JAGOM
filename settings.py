from default_settings import *
import os.path

TIME_ZONE = "Europe/Rome"
LANGUAGE_CODE = "it"
SECRET_KEY = "ei1yaks0h54mrcxdrt=le!-%k%+^-nppuo5h9euywio(np5ge+"

CONTACT_EMAIL = "info@jagom.org"
SITE_NAME = "JAGOM"

FORTUNE_BIN = "/usr/games/fortune"
FORTUNE_PATH = os.path.join(PROJECT_ROOT, "media", "quotes")

#Grain environment settings

PRJ_LINT_PATH = os.path.join(PROJECT_ROOT, "tracstuff", "000-LINTENV")
PRJ_ENV_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), "trac_venv")
PRJS_ENVS_PATH = os.path.join(PRJ_ENV_ROOT, "tracs")
PRJS_URL = "http://www.jagom.org/trac/"

NEW_PRJ_ENV_SCRIPT = os.path.join(PROJECT_ROOT, "bin", "new_project.sh")
UPDATE_PRJ_ENV_SCRIPT = os.path.join(PROJECT_ROOT, "bin", "update_project.sh")
CLONE_PRJ_ENV_SCRIPT = os.path.join(PROJECT_ROOT, "bin", "clone_project.sh")

from final_settings import *
