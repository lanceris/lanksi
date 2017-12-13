from django import forms
from patterns.models import TransactionTemplate
from accounts.models import Transaction

class PatternForm(forms.ModelForm):
    class Meta:
        model = TransactionTemplate
        exclude = ('owner', )

    def __init__(self, *args, **kwargs):
        self.transaction = kwargs.pop('transaction')
        self.owner = kwargs.pop('owner')
        super(PatternForm, self).__init__(*args, **kwargs)
        self.fields['transaction'].queryset = Transaction.objects.all()
        self.fields['transaction'].initial = self.transaction

    transaction = forms.ModelChoiceField(queryset=None)


class PatternEditForm(forms.ModelForm):
    class Meta:
        model = TransactionTemplate
        exclude = ('owner',)