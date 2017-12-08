from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^operation/add/(?P<slug>[-\w]+)$',          views.add_money,           name="add_money"),
    url(r'^operation/withdraw/(?P<slug>[-\w]+)$',     views.withdraw_money,      name="withdraw_money"),
    url(r'^operation/move/(?P<slug>[-\w]+)$',         views.move_money,          name="move_money"),
    url(r'^operation/exchange/(?P<slug>[-\w]+)$',     views.exchange_money,      name='exchange_money'),

    url(r'^$', views.list_, name='list_'),
    url(r'^add$', views.add, name='add'),
    url(r'^view/(?P<slug>[-\w]+)/$', views.details, name="details"),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.delete, name='delete'),
    url(r'^confirm-delete/(?P<slug>[-\w]+)$', views.confirm_delete, name='confirm_delete'),
]