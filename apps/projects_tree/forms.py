from django import forms
from pinax.apps.projects.forms import ProjectForm
from projects_tree.models import ProjectTree
from pinax.apps.projects.models import Project
from basic_groups.models import BasicGroup as Group

from django.conf import settings

class ProjectTreeForm(ProjectForm):

    language = forms.ChoiceField(choices=settings.LANGUAGES)

    #TODO: parent should have a "autocomplete search widget if clicked"
    parent = forms.ChoiceField() #, widget=forms.widgets.RadioSelect)
    member_groups = forms.MultipleChoiceField(widget=forms.widgets.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kw):
        super(ProjectTreeForm, self).__init__(*args, **kw)
        self.fields["parent"].choices = map(lambda x: (x.pk, x.name), Project.objects.filter(profile__is_clonable=True))
        self.fields["member_groups"].choices = map(lambda x: (x.pk, x.name), Group.objects.all()) 
        self.fields["language"].initial=settings.LANGUAGES[0][0]

    def clean_parent(self):
        return Project.objects.get(pk=int(self.data["parent"]))

    def clean_member_groups(self):
        return map(lambda pk: Group.objects.get(pk=int(pk)), self.data.get("member_groups",[]))
