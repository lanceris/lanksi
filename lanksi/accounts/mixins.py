from django import forms
from django.utils.translation import ugettext_lazy as _


class CategoryMixin(forms.Form):
    category = forms.ModelChoiceField(queryset=None,
                                      required=False,
                                      label=_("Category"))


class AccountMixin(forms.Form):
    account = forms.ModelChoiceField(queryset=None,
                                     label=_("Account"))