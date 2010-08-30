from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib import messages
from pinax.apps.projects.models import Project, ProjectMember

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

