from django.urls import path

from research import views

app_name = 'research'

urlpatterns = [
    path('', views.index, name='index'),
]