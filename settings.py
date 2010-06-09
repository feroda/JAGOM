from default_settings import *
import os.path

TIME_ZONE = "Europe/Rome"
LANGUAGE_CODE = "it"
SECRET_KEY = "ei1yaks0h54mrcxdrt=le!-%k%+^-nppuo5h9euywio(np5ge+"

CONTACT_EMAIL = "info@jagom.org"
SITE_NAME = "JAGOM"

FORTUNE_BIN = "/usr/games/fortune"
FORTUNE_PATH = os.path.join(PROJECT_ROOT, "media", "quotes")

#TRAC settings

TRACLINTPROJECT_PATH = os.path.join(PROJECT_ROOT, "tracstuff", "000-LINTENV")
TRACENV_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), "trac_venv")
TRACENVS_PATH = os.path.join(TRACENV_ROOT, "tracs")

NEW_TRAC_ENV_SCRIPT = os.path.join(PROJECT_ROOT, "bin", "new_trac_project.sh")
UPDATE_TRAC_ENV_SCRIPT = os.path.join(PROJECT_ROOT, "bin", "update_trac_project.sh")
CLONE_TRAC_ENV_SCRIPT = os.path.join(PROJECT_ROOT, "bin", "clone_trac_project.sh")

from final_settings import *
