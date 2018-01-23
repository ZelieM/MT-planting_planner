from django.urls import path

from . import views

app_name = 'planner'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_garden', views.create_garden, name='create_garden'),
    path('join_garden', views.join_garden, name='join_garden'),
    path('<int:garden_id>/', views.garden_view, name='garden_view')

]