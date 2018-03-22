from django.conf.urls import url
from django.urls import path

from django.contrib.auth import views as auth_views

from .views import *

app_name = 'planner'

urlpatterns = [
    path('', index, name='index'),

    # Authentications views
    url(r'^login/$', auth_views.login, {'template_name': 'planner/login.html'}, name='login'),
    path('signup', signup, name='signup'),
    # path('garden_selection', views.garden_selection, name='garden_selection'),
    path('garden_selection', custom_login_required(GardenSelectionView.as_view()), name='garden_selection'),
    path('logout', log_out, name="log_out"),

    # Beds management
    path('<int:garden_id>/add_bed', add_bed, name='add_bed'),
    path('<int:garden_id>/create_bed', custom_login_required(BedCreateView.as_view()), name='create_bed'),
    path('<int:garden_id>/update_bed/<int:pk>', custom_login_required(BedUpdateView.as_view()),
         name='update_bed'),
    path('<int:garden_id>/delete_bed/<int:pk>', custom_login_required(BedDelete.as_view()),
         name='delete_bed'),
    # path('<int:bedid>/delete_bed', views.delete_bed, name='delete_bed'),
    path('<int:garden_id>/', garden_view, name='garden_view'),
    path('<int:garden_id>/<int:area_id>/terminate_cropping',
         custom_login_required(DeactivateCultivatedArea.as_view()),
         name='deactivate_cultivated_area_view'),

    # Alerts views
    path('<int:garden_id>/alerts', custom_login_required(AlertView.as_view()), name='alerts_view'),
    path('<int:garden_id>/alerts/add_seed', add_seed, name='add_seed_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/validate', validate_alert, name='validate_alert_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/postpone', postpone_alert, name='postpone_alert_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/delete', delete_alert, name='delete_alert_view'),
    path('<int:garden_id>/alerts/add_punctual_operation', custom_login_required(AddPunctualOperationView.as_view()),
         name='add_punctual_operation'),
    path('<int:garden_id>/alerts/add_observation', custom_login_required(AddObservationView.as_view()),
         name='add_observation'),

    # Print Alerts view
    path('<int:garden_id>/alerts/print', custom_login_required(PrintForthcomingOperations.as_view()),
         name='print_forthcoming_operations'),


    # Vegetables view
    path('<int:garden_id>/vegetables', vegetables_view, name='vegetables_view'),
    path('<int:garden_id>/vegetables/new', custom_login_required(AddVegetableView.as_view()),
         name='add_vegetable_to_garden_view'),

    # Cultural operations management
    path('vegetables/delete_co/<int:co_id>', delete_co, name='delete_co'),
    path('<int:garden_id>/co/<int:co_id>', custom_login_required(EditCulturalOperationView.as_view()),
         name='edit_co_view'),
    path('<int:garden_id>/pick_co/<int:v_id>', pick_co_type, name='pick_co_type'),
    path('<int:garden_id>/<int:vegetable_id>/add_date_co',
         custom_login_required(CulturalOperationWithDateCreate.as_view()),
         name='add_date_co_view'),
    path('<int:garden_id>/<int:vegetable_id>/add_offset_co',
         custom_login_required(CulturalOperationWithOffsetCreate.as_view()),
         name='add_offset_co_view'),

    # Garden management
    path('<int:garden_id>/settings', garden_settings, name='garden_settings_view'),
    path('<int:garden_id>/settings/add_user', add_user_to_garden, name='add_user_to_garden_view'),
    path('<int:garden_id>/settings/delete/<int:user_id>', delete_user_from_garden,
         name='delete_user_from_garden'),
    path('<int:garden_id>/settings/notification_delay', edit_notification_delay, name='edit_notification_delay'),
    path('<int:garden_id>/settings/edit_email', custom_login_required(UserUpdate.as_view()),
         name='edit_user_email'),
    path('<int:garden_id>/settings/edit_details', custom_login_required(GardenDetailsUpdate.as_view()),
         name='garden_edit_details'),

    # Export pages
    path('<int:garden_id>/export', garden_export, name='garden_export_view'),
    path('<int:garden_id>/export/history', export_garden_history, name='export_garden_history'),

    # Statistics page
    path('<int:garden_id>/statistics', custom_login_required(GardenStatisticsView.as_view()),
         name='garden_statistics_view'),

    # Import from library view
    path('<int:garden_id>/import_vegetables', custom_login_required(ImportVegetablesView.as_view()),
         name='garden_import_vegetables_view'),
    path('<int:garden_id>/import_vegetables/select', custom_login_required(SelectVegetablesToImportView.as_view()),
         name='select_vegetables_to_import_view'),

]
