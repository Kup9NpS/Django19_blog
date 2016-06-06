from django import forms
from teams.models import Teams


class TeamUpdateForm(forms.ModelForm):

    class Meta:
        model = Teams
        fields = ('logo', 'title')

