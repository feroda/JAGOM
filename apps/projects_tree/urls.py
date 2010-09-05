from django.conf.urls.defaults import *

from pinax.apps.projects.models import Project
from pinax.apps.projects.urls import bridge

urlpatterns = patterns("",
    #Views useful for pinax developers (sent patch to them)
    url(r"^project/(?P<group_slug>[-\w]+)/delete-member/(?P<member_id>[-\w]+)/$", "projects_tree.views.delete_member", name="delete_member_from_project"),

    url(r"^create/$", "projects_tree.views.create", name="project_create"),

    url(r"^$", "pinax.apps.projects.views.projects", name="project_list"),
    url(r"^your_projects/$", "pinax.apps.projects.views.your_projects", name="your_projects"),
    # project-specific
    url(r"^project/(?P<group_slug>[-\w]+)/$", "pinax.apps.projects.views.project", name="project_detail"),
    url(r"^project/(?P<group_slug>[-\w]+)/delete/$", "pinax.apps.projects.views.delete", name="project_delete"),
)


