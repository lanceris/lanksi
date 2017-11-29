from django.conf.urls import url

from bank_accounts import views

urlpatterns = [
    url(r'^$', views.BankAccountListView.as_view(), name='list'),
]