from django.db import models

from pinax.apps.projects.models import Project
from basic_groups.models import BasicGroup
from django.utils.translation import ugettext_lazy as _

class ProjectTree(models.Model):

    project = models.OneToOneField(Project,
        related_name = "relations",
        verbose_name = _("project")
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
