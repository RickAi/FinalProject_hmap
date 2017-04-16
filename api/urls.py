from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^point_detail', views.point_detail, name='point_detail'),
    url(r'^points', views.points, name='points'),
    url(r'^boundaries', views.boundaries, name='boundaries'),
]