from django import forms
from pinax.apps.projects.forms import ProjectForm
from projects_tree.models import ProjectTree
from pinax.apps.projects.models import Project
from basic_groups.models import BasicGroup as Group

class ProjectTreeForm(ProjectForm):
    #TODO: parent should have a "autocomplete search widget if clicked"
    
    parent = forms.ChoiceField() #, widget=forms.widgets.RadioSelect)
    member_groups = forms.MultipleChoiceField(widget=forms.widgets.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kw):
        super(ProjectTreeForm, self).__init__(*args, **kw)
        self.fields["parent"].choices = map(lambda x: (x.pk, x.name), Project.objects.all())
        self.fields["member_groups"].choices = map(lambda x: (x.pk, x.name), Group.objects.all()) 

    def clean_parent(self):
        return Project.objects.get(pk=int(self.data["parent"]))

    def clean_member_groups(self):
        return map(lambda pk: Group.objects.get(pk=int(pk)), self.data["member_groups"])
