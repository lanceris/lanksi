from django import forms
from categories.models import Category
from django.conf import settings


class CategoryForm(forms.ModelForm):
    cat_type = forms.ChoiceField(choices=settings.TR_TYPES, required=False, label='Category type')
    name = forms.CharField(required=False, label='Name')

    class Meta:
        model = Category
        exclude = ('owner', )