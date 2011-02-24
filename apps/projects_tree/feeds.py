from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed
from pinax.apps.projects.models import Project

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

class MyLatestProjectFeed(LatestProjectFeed):
    title = _("My latest JAGOM projects")
    link = "/projects/your_projects/"
    description = _("My latest projects created in jagom.org")

    def get_object(self, request):
        user = request.user
        return Project.objects.filter(creator=user)

    def items(self, obj):
        return obj.order_by('-created')[:MAXPRJ]

