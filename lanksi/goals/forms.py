from django import forms
from goals.models import Goal
from decimal import Decimal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        exclude = ('owner', )


class AddMoneyForm(forms.Form):
    def __init__(self, **kwargs):
        self.goal = kwargs.pop('goal')
        super(AddMoneyForm, self).__init__(**kwargs)

    amount = forms.DecimalField(max_digits=26,
                                decimal_places=2,
                                min_value=0,
                                max_value=())