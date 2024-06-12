from django import forms
from web import models
from web.forms.bootstrap import BootStrapForm


class WikiForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project', 'depth',]
