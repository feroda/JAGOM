from django.conf import settings

from pinax.apps.projects.models import Project
import os

def get_base_project_for_language(language):
    default_slug = os.path.basename(settings.PRJ_LINT_PATH)
    base_slug_array =  default_slug.rsplit('-')
    base_project_slug = "-".join(base_slug_array[:-1] + [language])
    return Project.objects.get(slug=base_project_slug)

