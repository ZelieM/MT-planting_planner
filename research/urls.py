from django.urls import path

from research import views

app_name = 'research'

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.log_out, name="log_out"),
]