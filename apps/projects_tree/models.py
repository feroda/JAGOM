from django.db import models

from pinax.apps.projects.models import Project
from basic_groups.models import BasicGroup
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
import os.path

class ProjectTree(models.Model):
    """
    Project connections
    """

    project = models.OneToOneField(Project,
        related_name = "relations",
        verbose_name = _("project"),
        null=False
    )
    template = models.ForeignKey(Project,
        related_name = "instances",
        verbose_name = _("template")
    )

    member_groups = models.ManyToManyField(BasicGroup,
        verbose_name = _("groups")
    )
    
    def __unicode__(self):
        return u"%s from %s" % (self.project, self.template)

    class Meta:
        unique_together = [("template", "project")]

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
                   help_text=_("Make each JAGOM user able to update project notes and manage tickets"))

    def get_default_template(self):
        default_slug = os.path.basename(settings.PRJ_LINT_PATH)
        base_slug_array =  default_slug.rsplit('-')
        base_project_slug = "-".join(base_slug_array[:-1] + [self.language])
        return Project.objects.get(slug=base_project_slug)
