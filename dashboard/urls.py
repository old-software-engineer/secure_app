from django.conf.urls import url
from . import views

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^filter_tables', views.filter_tables, name="filter_tables"),
]
