from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^point_detail', views.point_detail, name='point_detail'),
    url(r'^points', views.points, name='points'),
    url(r'^boundaries', views.boundaries, name='boundaries'),
    url(r'^overall_housecount', views.overall_housecount, name='overall_housecount'),
    url(r'^overall_avgroi', views.overall_avgroi, name='overall_avgroi'),
    url(r'^boundary_housetype', views.boundary_housetype, name='boundary_housetype'),
]