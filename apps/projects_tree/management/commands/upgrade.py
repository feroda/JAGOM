 
# Copyright (C) 2010 BeFair snc <http://www.befair.it>
#
# This file is part of JAGOM
# JAGOM is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# JAGOM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with JAGOM. If not, see <http://www.gnu.org/licenses/>.


from django.core.management.base import BaseCommand, NoArgsCommand, CommandError
from django.core.management.color import no_style
from optparse import make_option
from django.conf import settings

from pinax.apps.projects.models import Project
from projects_tree.models import ProjectTree, ProjectProfile

class Command(NoArgsCommand):

    help = "Performs sanity check and upgrade"

    def handle(self, *args, **kw):

        if settings.VERSION[:1] == (0,1):
            try:
                default_parent = Project.objects.get(slug=settings.PRJ_LINT_SLUG)
            except Project.DoesNotExist:
                # Older versions named 000-LINTENV to mean 000-LINTENV-it
                default_parent = Project.objects.get(slug="000-LINTENV")
                default_parent.slug = "000-LINTENV-it"
                default_parent.save()

            for p in Project.objects.all():
                try:
                    assert p.relations
                except ProjectTree.DoesNotExist:
                    #Set base project (default is italian language)
                    
                    project_tree = ProjectTree(project=p, parent=default_parent)
                    project_tree.save()

                try:
                    assert p.profile
                except ProjectProfile.DoesNotExist:
                    project_profile = ProjectProfile(project=p, language="it")
                    project_profile.save()

