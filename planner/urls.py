from django.conf.urls import url
from django.urls import path


from django.contrib.auth import views as auth_views

from . import views
from .views import CulturalOperationCreate

app_name = 'planner'
urlpatterns = [
    path('', views.index, name='index'),

    url(r'^login/$', auth_views.login, {'template_name': 'planner/login.html'}, name='login'),

    path('signup', views.signup, name='signup'),
    path('garden_selection', views.garden_selection, name='garden_selection'),
    path('join_garden', views.join_garden, name='join_garden'),
    path('logout', views.log_out, name="log_out"),
    path('<int:gardenid>/add_bed', views.add_bed, name='add_bed'),
    path('<int:bedid>/delete_bed', views.delete_bed, name='delete_bed'),
    path('<int:garden_id>/', views.garden_view, name='garden_view'),
    path('<int:garden_id>/alerts', views.alerts_view, name='alerts_view'),
    path('<int:garden_id>/vegetables', views.vegetables_view, name='vegetables_view'),
    path('vegetables/delete_co/<int:co_id>', views.delete_co, name='delete_co'),
    path('<int:garden_id>/co/<int:co_id>', views.edit_co_view, name='edit_co_view'),
    path('<int:garden_id>/<int:vegetable_id>/add_co', CulturalOperationCreate.as_view(), name='add_co_view'),
]
