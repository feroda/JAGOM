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
from projects_tree.forms import ProjectTreeForm
from projects_tree.models import ProjectTree

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
        # Save parent and members group
        parent = project_form.cleaned_data['parent']
        member_groups = project_form.cleaned_data['member_groups']
        project_tree = ProjectTree(project=project, parent=parent)
        project_tree.save()
        for g in member_groups:
            project_tree.member_groups.add(g)
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
    return HttpResponse("OK")

