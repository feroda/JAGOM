from django.db import models

from pinax.apps.projects.models import Project
from basic_groups.models import BasicGroup
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

class ProjectTree(models.Model):
    """
    Project connections
    """

    project = models.OneToOneField(Project,
        related_name = "relations",
        verbose_name = _("project"),
        null=False
    )
    parent = models.ForeignKey(Project,
        related_name = "children",
        verbose_name = _("cloned from")
    )

    member_groups = models.ManyToManyField(BasicGroup,
        verbose_name = _("groups")
    )
    
    class Meta:
        unique_together = [("parent", "project")]

class ProjectProfile(models.Model):
    """
    Extend project attributes
    """

    project = models.OneToOneField(Project,
        related_name = "profile",
        verbose_name = _("project"),
        null=False
    )

    is_clonable = models.BooleanField(default=False)
    language = models.CharField(max_length=32, choices=settings.LANGUAGES)
    open_updates = models.BooleanField(default=True, 
                   help_text=_("Let each user able to update project notes and manage tickets"))

