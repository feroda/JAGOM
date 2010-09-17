from django import forms
from django.utils.translation import ugettext_lazy as _
from pinax.apps.projects.forms import ProjectForm
from projects_tree.models import ProjectTree
from pinax.apps.projects.models import Project
from basic_groups.models import BasicGroup as Group

from django.conf import settings

class ProjectTreeForm(ProjectForm):

    language = forms.ChoiceField(choices=settings.LANGUAGES)

#    member_groups = forms.MultipleChoiceField(widget=forms.widgets.CheckboxSelectMultiple, required=False)

    open_updates = forms.BooleanField(required=False, initial=False,
                   help_text=_("Make each JAGOM user able to update project notes and manage tickets")
    )

    def __init__(self, *args, **kw):
        super(ProjectTreeForm, self).__init__(*args, **kw)
#        self.fields["member_groups"].choices = map(lambda x: (x.pk, x.name), Group.objects.all()) 
        self.fields["language"].initial=settings.LANGUAGES[0][0]

    def clean_parent(self):
        return Project.objects.get(pk=int(self.data["parent"]))

#    def clean_member_groups(self):
#        return map(lambda pk: Group.objects.get(pk=int(pk)), self.data.get("member_groups",[]))


# TODO: This is temporary ! 
# Used only because AddUserForm.save does not issue a signal 
from pinax.apps.projects.forms import AddUserForm
from tracstuff.models import update_members_list

class MyAddUserForm(AddUserForm):

    def save(self, *args, **kw):
        rv = super(MyAddUserForm, self).save(*args, **kw)
        update_members_list(sender=None, instance=self.project)
        return rv
