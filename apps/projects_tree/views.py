from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template import RequestContext
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from pinax.apps.projects.models import Project, ProjectMember
from pinax.apps.projects.views import create as pinax_project_create
from pinax.apps.projects.views import project as pinax_project_project
from projects_tree.forms import ProjectTreeForm
from projects_tree.forms import MyAddUserForm
from projects_tree.models import ProjectTree, ProjectProfile

from projects_tree import get_base_project_for_language

#FIXME: will not be necessary when we will issue a signal upon member deletion
from tracstuff.models import update_members_list

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

@login_required
def create(request, form_class=ProjectTreeForm, template_name="projects/create.html"):
    project_form = form_class(request.POST or None)
    
    if project_form.is_valid():
        project = project_form.save(commit=False)
        project.creator = request.user
        project.save()
        project_member = ProjectMember(project=project, user=request.user)
        project.members.add(project_member)
        project_member.save()

        language = project_form.cleaned_data['language']
        open_updates = project_form.cleaned_data['open_updates']

        # Save parent and members group
        parent = project_form.cleaned_data.get('parent', 
                    get_base_project_for_language(language)
        )
        project_tree = ProjectTree(project=project, parent=parent)
        project_tree.save()
#        member_groups = project_form.cleaned_data['member_groups']
#        for g in member_groups:
#            project_tree.member_groups.add(g)

        # Save xattr: after saving project relations
        project_profile = ProjectProfile(project=project, 
                            language=language, 
                            open_updates=open_updates
                          )
        project_profile.save()

        if notification:
            # @@@ might be worth having a shortcut for sending to all users
            notification.send(User.objects.all(), "projects_new_project",
                {"project": project}, queue=True)
        return HttpResponseRedirect(project.get_absolute_url())
    
    return render_to_response(template_name, {
        "project_form": project_form,
    }, context_instance=RequestContext(request))
        

def delete_member(request, group_slug, member_id):
    projectmember = get_object_or_404(ProjectMember, pk=member_id)
    projectmember.delete()
    messages.add_message(request, messages.SUCCESS,
        ugettext("Member %(user)s has been removed from project %(project_name)s deleted.") % {
            "user": projectmember.user,
            "project_name": projectmember.project.name,
        }
    )
    #TODO: issue a signal
    update_members_list(sender=None, instance=projectmember.project)

    return HttpResponse("OK")

def project(request, adduser_form_class=MyAddUserForm, **kw):

    return pinax_project_project(request, adduser_form_class=adduser_form_class, **kw)
