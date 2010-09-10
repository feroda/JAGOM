from django.db import models
from django.conf import settings

from projects_tree.models import ProjectProfile
import subprocess, os, sys

env = os.environ
encoding = 'latin-1'

def activate_trac_env(sender, **kwargs):

    env['JAGOM_HOME'] = settings.PROJECT_ROOT
    env['PYTHONPATH'] = ':'.join(sys.path)
    instance = kwargs['instance']
    prj = instance.project
    slug = prj.slug.encode(encoding) 
    name = prj.name.encode(encoding) 
    description = prj.description.encode(encoding) 

    if kwargs['created']:
        parent = prj.relations.parent.slug
        subprocess.Popen([ 
            settings.NEW_PRJ_ENV_SCRIPT, 
            slug, prj.creator.username, name, description, parent
        ], env=env)

    else:
        subprocess.Popen([
            settings.UPDATE_PRJ_ENV_SCRIPT,
            slug, name, description
        ], env=env)

    #TODO: Check for errors that happen in scripts
        
    return True

models.signals.post_save.connect(activate_trac_env, sender=ProjectProfile)
