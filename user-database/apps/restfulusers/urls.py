from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^users$', views.index1),
	url(r'^users/(?P<id>\d+)$', views.show, name='show'),
	url(r'^new$', views.new, name='new'),
	url(r'^users/(?P<id>\d+)/edit$', views.edit, name='edit'),
	url(r'^goback$', views.index, name='goback'),
	url(r'^update/(?P<id>\d+)$', views.update),
	url(r'^create$', views.create, name='create'),
	url(r'^users/(?P<id>\d+)/delete$', views.delete, name='delete'),
]