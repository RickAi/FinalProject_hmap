from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^', views.cluster_map, name='index'),
    url(r'^cluster_map', views.cluster_map, name='cluster_map'),
    url(r'^point_map', views.point_map, name='point_map'),
    url(r'^heat_map', views.heat_map, name='heat_map'),
    url(r'^choropleth_map', views.choropleth_map, name='choropleth_map'),
]