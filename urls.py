from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from tagging.models import TaggedItem
from wakawaka.models import WikiPage

from pinax.apps.account.openid_consumer import PinaxConsumer
from pinax.apps.projects.models import Project
from pinax.apps.tasks.models import Task
from pinax.apps.topics.models import Topic


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "intro.html",
    }, name="intro"),
    
    url(r"^home/$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    
    #JAGOM specific views
    url(r"^projects/", include("projects_tree.urls")),
    
    #Views useful for pinax developers (sent patch to them)
    url(r"^get_messages/$", "base.views.get_messages", name="get_messages"),

    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/(.*)", PinaxConsumer()),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r"^tagging_utils/", include("pinax.apps.tagging_utils.urls")),
    url(r"^comments/", include("threadedcomments.urls")),
    url(r"^attachments/", include("attachments.urls")),
    url(r"^groups/", include("basic_groups.urls")),
    url(r"^tribes/", include("pinax.apps.tribes.urls")),
    url(r"^flag/", include("flag.urls")),

    (r'^i18n/', include('django.conf.urls.i18n')),

    #WAS 0.9.dev12: url(r"^account/signup/$", signup_view, name="acct_signup"),

    url(r"^get_fortune/", "fortune.views.get_fortune", name="get_fortune"),
    url(r"^feed_proxy/", "feed_proxy.views.get_feed", name="feed_proxy"),
)


tagged_models = (
    dict(title="Projects",
        query=lambda tag: TaggedItem.objects.get_by_model(Project, tag),
    ),
    dict(title="Topics",
        query=lambda tag: TaggedItem.objects.get_by_model(Topic, tag),
    ),
    dict(title="Project Tasks",
        query=lambda tag: TaggedItem.objects.get_by_model(Task, tag),
    ),
    dict(title="Wiki Articles",
        query=lambda tag: TaggedItem.objects.get_by_model(WikiPage, tag),
    ),
        

)
tagging_ext_kwargs = {
  "tagged_models": tagged_models,
}

urlpatterns += patterns("",
  url(r"^tags/(?P<tag>.+)/(?P<model>.+)$", "tagging_ext.views.tag_by_model",
        kwargs=tagging_ext_kwargs, name="tagging_ext_tag_by_model"),
  url(r"^tags/(?P<tag>.+)/$", "tagging_ext.views.tag",
        kwargs=tagging_ext_kwargs, name="tagging_ext_tag"),
  url(r"^tags/$", "tagging_ext.views.index", name="tagging_ext_index"),
)



if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
