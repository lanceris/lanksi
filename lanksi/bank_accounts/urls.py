from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from bank_accounts import views

urlpatterns = [
    url(r'^register/$',                               views.register,            name='register'),

    url(r'^$',                                        views.list_accounts,       name='list_accounts'),
    url(r'^account/add$',                             views.add_account,         name="add_account"),
    url(r'^account/view/(?P<slug>[-\w]+)/$',          views.account_details,     name="account_details"),
    url(r'^account/edit/(?P<slug>[-\w]+)/$',          views.edit_account,        name="edit_account"),
    url(r'^account/delete/(?P<slug>[-\w]+)/$',        views.delete_account,      name='delete_account'),
    url(r'^account/delete/confirm/(?P<slug>[-\w]+)$', views.confirm_delete,      name='confirm_delete'),

    url(r'^operation/add/(?P<slug>[-\w]+)$',          views.add_money,           name="add_money"),
    url(r'^operation/withdraw/(?P<slug>[-\w]+)$',     views.withdraw_money,      name="withdraw_money"),
    url(r'^operation/move/(?P<slug>[-\w]+)$',         views.move_money,          name="move_money"),
]