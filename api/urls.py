from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^point_detail', views.point_detail, name='point_detail'),
]