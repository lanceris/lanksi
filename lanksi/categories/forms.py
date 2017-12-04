from django import forms
from categories.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('owner', )


class EditCategoryForm(forms.Form):
    name = forms.CharField(required=False)

    class Meta:
        model = Category
        exclude = ('owner', )