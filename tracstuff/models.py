from django.db import models
from django.conf import settings

from pinax.apps.projects.models import Project
import subprocess, os

env = os.environ
def activate_trac_env(sender, **kwargs):

    env['JAGOM_HOME'] = settings.PROJECT_ROOT
    prj = kwargs['instance']

    if kwargs['created']:
        subprocess.Popen([ 
            settings.NEW_TRAC_ENV_SCRIPT, 
            prj.slug, prj.name, prj.description
        ], env=env)

    else:
        subprocess.Popen([
            settings.UPDATE_TRAC_ENV_SCRIPT,
            prj.slug, prj.name, prj.description
        ], env=env)

    #TODO: Check for errors
        
    return True

models.signals.post_save.connect(activate_trac_env, sender=Project)
