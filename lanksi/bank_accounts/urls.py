from django.conf.urls import url

from bank_accounts import views

urlpatterns = [
    url(r'^$', views.list_accounts, name='list_accounts'),
    url(r'^account/view/(?P<slug>[-\w]+)/$', views.account_details, name="account_details"),
    url(r'^account/add$', views.add_account, name="add_account"),
    url(r'^operation/add/(?P<slug>[-\w]+)$', views.add_money, name="add_money"),
    url(r'^operation/withdraw/(?P<slug>[-\w]+)$', views.withdraw_money, name="withdraw_money"),
    url(r'^operation/move/(?P<slug>[-\w]+)$', views.move_money, name="move_money"),
    url(r'^history/(?P<slug>[-\w]+)$', views.history, name="history"),
]