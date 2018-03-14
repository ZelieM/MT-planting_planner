from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
from .views import CulturalOperationWithDateCreate, CulturalOperationWithOffsetCreate, AlertView, GardenSelectionView, \
    EditCulturalOperationView, AddObservationView, AddPunctualOperationView, AddVegetableView, GardenStatisticsView, \
    ImportVegetablesView, SelectVegetablesToImportView

app_name = 'planner'

urlpatterns = [
    path('', views.index, name='index'),

    # Authentications views
    url(r'^login/$', auth_views.login, {'template_name': 'planner/login.html'}, name='login'),
    path('signup', views.signup, name='signup'),
    # path('garden_selection', views.garden_selection, name='garden_selection'),
    path('garden_selection', login_required(GardenSelectionView.as_view()), name='garden_selection'),
    path('join_garden', views.join_garden, name='join_garden'),
    path('logout', views.log_out, name="log_out"),

    # Beds management
    path('<int:garden_id>/add_bed', views.add_bed, name='add_bed'),
    path('<int:bedid>/delete_bed', views.delete_bed, name='delete_bed'),
    path('<int:garden_id>/', views.garden_view, name='garden_view'),

    # Alerts views
    # path('<int:garden_id>/alerts', views.alerts_view, name='alerts_view'),
    path('<int:garden_id>/alerts', login_required(AlertView.as_view()), name='alerts_view'),
    path('<int:garden_id>/alerts/add_seed', views.add_seed, name='add_seed_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/validate', views.validate_alert, name='validate_alert_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/postpone', views.postpone_alert, name='postpone_alert_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/delete', views.delete_alert, name='delete_alert_view'),
    # path('<int:garden_id>/alerts/add_punctual_operation', views.add_punctual_operation, name='add_punctual_operation'),
    path('<int:garden_id>/alerts/add_punctual_operation', login_required(AddPunctualOperationView.as_view()),
         name='add_punctual_operation'),
    # path('<int:garden_id>/alerts/add_observation', views.add_observation, name='add_observation'),
    path('<int:garden_id>/alerts/add_observation', login_required(AddObservationView.as_view()),
         name='add_observation'),

    # Vegetables view
    path('<int:garden_id>/vegetables', views.vegetables_view, name='vegetables_view'),
    path('<int:garden_id>/vegetables/new', login_required(AddVegetableView.as_view()),
         name='add_vegetable_to_garden_view'),

    # Cultural operations management
    path('vegetables/delete_co/<int:co_id>', views.delete_co, name='delete_co'),
    path('<int:garden_id>/co/<int:co_id>', login_required(EditCulturalOperationView.as_view()), name='edit_co_view'),
    path('<int:garden_id>/pick_co/<int:v_id>', views.pick_co_type, name='pick_co_type'),
    path('<int:garden_id>/<int:vegetable_id>/add_date_co', login_required(CulturalOperationWithDateCreate.as_view()),
         name='add_date_co_view'),
    path('<int:garden_id>/<int:vegetable_id>/add_offset_co',
         login_required(CulturalOperationWithOffsetCreate.as_view()),
         name='add_offset_co_view'),

    # Garden management
    path('<int:garden_id>/settings', views.garden_settings, name='garden_settings_view'),
    path('<int:garden_id>/settings/add_user', views.add_user_to_garden, name='add_user_to_garden_view'),
    path('<int:garden_id>/settings/delete/<int:user_id>', views.delete_user_from_garden,
         name='delete_user_from_garden'),
    path('<int:garden_id>/settings/notification_delay', views.edit_notification_delay, name='edit_notification_delay'),

    # Export pages
    path('<int:garden_id>/export', views.garden_export, name='garden_export_view'),
    path('<int:garden_id>/export/history', views.export_garden_history, name='export_garden_history'),

    # Statistics page
    path('<int:garden_id>/statistics', login_required(GardenStatisticsView.as_view()), name='garden_statistics_view'),

    # Import from library view
    path('<int:garden_id>/import_vegetables', login_required(ImportVegetablesView.as_view()),
         name='garden_import_vegetables_view'),
    path('<int:garden_id>/import_vegetables/select', login_required(SelectVegetablesToImportView.as_view()),
         name='select_vegetables_to_import_view'),

]
