from django import forms
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _


class CategoryMixin(forms.Form):
    category = forms.ModelChoiceField(queryset=None,
                                      required=False,
                                      label=_("Category"))


class AccountMixin(forms.Form):
    account = forms.ModelChoiceField(queryset=None,
                                     label=_("Account"))


class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response