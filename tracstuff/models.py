from django.db import models
from django.conf import settings

from pinax.apps.projects.models import Project
import subprocess, os, sys

env = os.environ
encoding = 'latin-1'

def activate_trac_env(sender, **kwargs):

    env['JAGOM_HOME'] = settings.PROJECT_ROOT
    env['PYTHONPATH'] = ':'.join(sys.path)
    prj = kwargs['instance']
    slug = prj.slug.encode(encoding) 
    name = prj.name.encode(encoding) 
    description = prj.description.encode(encoding) 
    #TODO: language support per project 
    language_code = getattr(prj, "language_code", settings.LANGUAGE_CODE)
    #TODO: projects can inherit from other projects rather than always inheriting from LINTENV
    #FIXME: should be set the default id rather than PRJ_LINT_PATH as default
    parent = getattr(prj, "parent", settings.PRJ_LINT_PATH)

    if kwargs['created']:
        subprocess.Popen([ 
            settings.NEW_PRJ_ENV_SCRIPT, 
            slug, language_code, name, description
        ], env=env)

    else:
        subprocess.Popen([
            settings.UPDATE_PRJ_ENV_SCRIPT,
            slug, name, description
        ], env=env)

    #TODO: Check for errors
        
    return True

models.signals.post_save.connect(activate_trac_env, sender=Project)
