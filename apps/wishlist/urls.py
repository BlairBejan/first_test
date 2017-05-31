from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
    url(r'^/create$', views.addpage),
    url(r'^/makeitem$', views.makeitem),
    url(r'^/item/(?P<id>\d+)$', views.item),
    url(r'^/additem/(?P<id>\d+)$', views.additem),
    url(r'^/deleteitem/(?P<itemid>\d+)$', views.deleteitem),
    url(r'^/removefromwishlist/(?P<itemid>\d+)$', views.removefromlist),
]
