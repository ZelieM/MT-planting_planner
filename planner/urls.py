from django.conf.urls import url
from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
from .views import CulturalOperationWithDateCreate, CulturalOperationWithOffsetCreate

app_name = 'planner'
urlpatterns = [
    path('', views.index, name='index'),

    # Authentications views
    url(r'^login/$', auth_views.login, {'template_name': 'planner/login.html'}, name='login'),
    path('signup', views.signup, name='signup'),
    path('garden_selection', views.garden_selection, name='garden_selection'),
    path('join_garden', views.join_garden, name='join_garden'),
    path('logout', views.log_out, name="log_out"),

    # Beds management
    path('<int:garden_id>/add_bed', views.add_bed, name='add_bed'),
    path('<int:bedid>/delete_bed', views.delete_bed, name='delete_bed'),
    path('<int:garden_id>/', views.garden_view, name='garden_view'),

    # Alerts views
    path('<int:garden_id>/alerts', views.alerts_view, name='alerts_view'),
    path('<int:garden_id>/alerts/add_seed', views.add_seed, name='add_seed_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/validate', views.validate_alert, name='validate_alert_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/postpone', views.postpone_alert, name='postpone_alert_view'),

    # Vegetables view
    path('<int:garden_id>/vegetables', views.vegetables_view, name='vegetables_view'),

    # Cultural operations management
    path('vegetables/delete_co/<int:co_id>', views.delete_co, name='delete_co'),
    path('<int:garden_id>/co/<int:co_id>', views.edit_co_view, name='edit_co_view'),
    path('<int:garden_id>/pick_co/<int:v_id>', views.pick_co_type, name='pick_co_type'),
    path('<int:garden_id>/<int:vegetable_id>/add_date_co', CulturalOperationWithDateCreate.as_view(),
         name='add_date_co_view'),
    path('<int:garden_id>/<int:vegetable_id>/add_offset_co', CulturalOperationWithOffsetCreate.as_view(),
         name='add_offset_co_view'),

    # Garden management
    path('<int:garden_id>/settings', views.garden_settings, name='garden_settings_view'),
    path('<int:garden_id>/settings/add_user', views.add_user_to_garden, name='add_user_to_garden_view'),
]
