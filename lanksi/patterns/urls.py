from django.conf.urls import url
from patterns import views

urlpatterns = [
    url(r'^$', views.list_, name='list_'),
    url(r'^add$', views.add, name='add'),
    url(r'^view/(?P<slug>[-\w]+)/$', views.details, name="details"),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.delete, name='delete'),
    url(r'^confirm-delete/(?P<slug>[-\w]+)$', views.confirm_delete, name='confirm_delete'),
]