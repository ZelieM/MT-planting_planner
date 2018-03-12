from django.urls import path

from vegetables_library import views

app_name = 'vegetables_library'


urlpatterns = [
    path('', views.index, name='index'),
]