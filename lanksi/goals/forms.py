from django import forms
from goals.models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        exclude = ('owner', )


class EditGoalForm(forms.Form):
    name = forms.CharField(required=False)

    class Meta:
        model = Goal
        exclude = ('owner', )
