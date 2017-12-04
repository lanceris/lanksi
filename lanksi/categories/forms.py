from django import forms
from categories.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('owner', )


class EditCategoryForm(forms.Form):
    cat_type = forms.IntegerField(min_value=1, max_value=4)
    name = forms.CharField()

    class Meta:
        model = Category
        exclude = ('owner', )