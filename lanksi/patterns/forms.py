from django import forms
from patterns.models import TransactionTemplate


class PatternForm(forms.ModelForm):
    class Meta:
        model = TransactionTemplate
        exclude = ('owner', )

    def __init__(self, *args, **kwargs):
        self.transaction = kwargs.pop('transaction')
        super(PatternForm, self).__init__(*args, **kwargs)