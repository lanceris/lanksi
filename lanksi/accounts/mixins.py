from django import forms
from django.utils.translation import ugettext_lazy as _


class DescriptionMixin(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 50}),
                                  required=False,
                                  label=_("Description"))


class CommentMixin(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 50}),
                                  required=False,
                                  label=_("Comment"))


class CategoryMixin(forms.Form):
    category = forms.ModelChoiceField(queryset=None,
                                      required=False,
                                      label=_("Category"))


class AccountMixin(forms.Form):
    account = forms.ModelChoiceField(queryset=None,
                                     label=_("Account"))