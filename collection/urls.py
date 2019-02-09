from django.urls import path, re_path
from . import views


app_name = 'collection'

urlpatterns = [
    re_path(r'^add/(?P<card_id>\d+)/$', views.add_card_to_collection, name='collection_add'),
    re_path(r'^remove/(?P<card_id>\d+)/$', views.remove_card_from_collection, name='collection_remove'),
    re_path(r'^create/$', views.collection_create, name='collection_create'),
    re_path(r'^(?P<user_name>[-\w]+)/(?P<collection_slug>[-\w]+)/$', views.collection_view, name='collection_view'),
]
