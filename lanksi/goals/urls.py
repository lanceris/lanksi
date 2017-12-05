from django.conf.urls import url
from goals import views

urlpatterns = [
    url(r'^$', views.list_, name='list_'),
    url(r'^add$', views.add, name='add'),
    url(r'^add_money/(?P<id>[-\d]+)/$', views.add_money, name='add_money'),
    url(r'^view/(?P<id>[-\d]+)/$', views.details, name="details"),
    url(r'^edit/(?P<id>[-\d]+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<id>[-\d]+)/$', views.delete, name='delete'),
    url(r'^confirm-delete/(?P<id>[-\d]+)$', views.confirm_delete, name='confirm_delete'),
]