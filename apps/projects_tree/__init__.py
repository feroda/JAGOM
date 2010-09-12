from django.conf import settings

from pinax.apps.projects.models import Project

def get_base_project_for_language(language):
    array =  settings.PRJ_LINT_PATH.rsplit('-')
    array[-1] = language
    base_project_slug = "-".join(array)
    return Project.objects.get(slug=base_project_slug)

