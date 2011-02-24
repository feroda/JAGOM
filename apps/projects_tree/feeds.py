from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed
from pinax.apps.projects.models import Project
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

MAXPRJ=10

class LatestProjectFeed(Feed):
    title = _("Latest JAGOM projects")
    link = "/projects/"
    description = _("Latest projects created in jagom.org")

    def items(self):
        return Project.objects.order_by('-created')[:MAXPRJ]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

class UserLatestProjectFeed(Feed):

    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return _("JAGOM.org: latest projects for user %s") % obj

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return _("Latest projects for user %s") % obj

    def items(self, obj):
        return Project.objects.filter(creator=obj)[:MAXPRJ]

