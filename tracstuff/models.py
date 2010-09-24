from django.db import models
from django.conf import settings

from projects_tree.models import ProjectProfile, ProjectTree
from pinax.apps.projects.models import Project
import subprocess, os, sys
import base

encoding = 'latin-1'

def activate_trac_env(sender, **kwargs):
    """
    Clone project environment as soon as a project has been created
    """

    instance = kwargs['instance']
    prj = instance.project
    slug = prj.slug.encode(encoding) 
    name = prj.name.encode(encoding) 
    description = prj.description.encode(encoding) 

    if kwargs['created']:
        base.log.debug("New project %s created" % prj)
        try:
            parent_slug = prj.relations.parent.slug
        except ProjectTree.DoesNotExist:
            raise
        parent_path = os.path.join(settings.PRJS_ENVS_PATH, parent_slug)
        creator = prj.creator.username
        base.log.debug("slug=%s, creator=%s, name=%s, parent_path=%s" % (slug, creator, name, parent_path))
        base.execute_and_log([ 
            settings.NEW_PRJ_ENV_SCRIPT, 
            slug, creator, name, description, parent_path,
        ])

    else:
        base.log.debug("Project %s: info updated" % prj)
        base.execute_and_log([ 
            settings.UPDATE_PRJ_ENV_SCRIPT,
            slug, name, description
        ])

    return True

models.signals.post_save.connect(activate_trac_env, sender=ProjectProfile)

def deactivate_trac_env(sender, **kwargs):
    """
    Deactivate project environment. Rename it to .slug.old
    """

    instance = kwargs['instance']
    prj = instance.project
    slug = prj.slug.encode(encoding) 
    prj_path = os.path.join(settings.PRJS_ENVS_PATH, slug)
#    c = 1
#    while c:
#        # It may be deleted in the past, created again and deleting now
    try:
        #dst = "%s/.%s.%d" % (settings.PRJS_ENVS_PATH,slug, c)
        dst = "%s/.%s" % (settings.PRJS_ENVS_PATH,slug)
        base.log.debug("Project %s removed. Moving data to %s" % (prj, dst))
        os.rename(prj_path, dst)
    except OSError:
#        c += 1
        pass
#    else:
#        break
        
    return True

models.signals.post_delete.connect(deactivate_trac_env, sender=ProjectProfile)

def update_members_list(sender, **kwargs):
    """
    Update members list in the project environment
    """

    instance = kwargs['instance']
    prj = instance
    members = prj.members.all()

    admins = []
    users = []

    for m in members:
        # TODO: get flag for members role in project and then invoke 
        # update_members and update_administrators script.
        # In 0.1 all members are admins !
        if 1: #m.is_admin=True 
            admins.append(m.user.username)
        else:
            users.append(m.user.username)
        
    if users:
        base.execute_and_log([ 
            settings.UPDATE_PRJ_MEMBERS_SCRIPT, 
            prj.slug ] + users
        )

    if admins:
        base.execute_and_log([ 
            settings.UPDATE_PRJ_ADMINS_SCRIPT, 
            prj.slug ] + admins
        )
    return True

#models.signals.m2m_changed.connect(update_members_list, sender=Project.member_users.through)


