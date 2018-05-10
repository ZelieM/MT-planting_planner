from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from planner.custom_decorators import access_private_garden, custom_login_required
from .views import *

app_name = 'planner'

urlpatterns = [
    path('', index, name='index'),

    # Authentications views
    url(r'^login/$', auth_views.login, {'template_name': 'planner/login.html'}, name='login'),
    path('signup', signup, name='signup'),
    path('garden_selection', custom_login_required(GardenSelectionView.as_view()), name='garden_selection'),
    path('logout', log_out, name="log_out"),

    # Beds management
    path('<int:garden_id>/create_bed', access_private_garden(BedCreateView.as_view()), name='create_bed'),
    path('<int:garden_id>/update_bed/<int:pk>', access_private_garden(BedUpdateView.as_view()),
         name='update_bed'),
    path('<int:garden_id>/delete_bed/<int:pk>', access_private_garden(BedDelete.as_view()),
         name='delete_bed'),
    path('<int:garden_id>', access_private_garden(GardenView.as_view()), name='garden_view'),
    path('<int:garden_id>/save_bed_position', access_private_garden(SaveBedPosition.as_view()), name='save_bed_position'),

    # QR codes logic
    path('<int:garden_id>/qr/<int:pk>', access_private_garden(BedQRView.as_view()), name="qr_bed_view"),
    path('<int:garden_id>/qr_area/<int:pk>', access_private_garden(OperationByAreaQRView.as_view()),
         name="qr_area_view"),
    path('<int:garden_id>/print_qr', access_private_garden(PrintQRView.as_view()), name="print_qr_codes"),

    # Crops management
    path('<int:garden_id>/crops', access_private_garden(CropsIndexView.as_view()), name='crops_view'),
    path('<int:garden_id>/<int:area_id>/terminate_cropping',
         access_private_garden(DeactivateCultivatedArea.as_view()),
         name='deactivate_cultivated_area_view'),

    # Alerts views
    path('<int:garden_id>/alerts', access_private_garden(AlertView.as_view()), name='alerts_view'),
    path('<int:garden_id>/alerts/add_seed', access_private_garden(AddSeed.as_view()), name='add_seed_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/validate', access_private_garden(ValidateAlert.as_view()),
         name='validate_alert_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/postpone', access_private_garden(PostponeAlert.as_view()),
         name='postpone_alert_view'),
    path('<int:garden_id>/alerts/<int:alert_id>/delete', access_private_garden(DeleteAlert.as_view()),
         name='delete_alert_view'),
    path('<int:garden_id>/alerts/add_punctual_operation',
         access_private_garden(AddPunctualOperationView.as_view()),
         name='add_punctual_operation'),
    path('<int:garden_id>/alerts/add_observation', access_private_garden(AddObservationView.as_view()),
         name='add_observation'),

    # Print Alerts view
    path('<int:garden_id>/alerts/print', access_private_garden(PrintForthcomingOperations.as_view()),
         name='print_forthcoming_operations'),

    # Vegetables view
    path('<int:garden_id>/vegetables', access_private_garden(VegetablesView.as_view()), name='vegetables_view'),
    path('<int:garden_id>/vegetables/new', access_private_garden(AddVegetableView.as_view()),
         name='add_vegetable_to_garden_view'),

    # Cultural operations management
    path('<int:garden_id>/vegetables/delete_co/<int:co_id>', access_private_garden(CulturalOperationDelete.as_view()),
         name='delete_co'),
    path('<int:garden_id>/co/<int:co_id>', access_private_garden(EditCulturalOperationView.as_view()),
         name='edit_co_view'),
    path('<int:garden_id>/pick_co/<int:v_id>', access_private_garden(PickCOType.as_view()), name='pick_co_type'),
    path('<int:garden_id>/<int:vegetable_id>/add_date_co',
         access_private_garden(CulturalOperationWithDateCreate.as_view()),
         name='add_date_co_view'),
    path('<int:garden_id>/<int:vegetable_id>/add_offset_co',
         access_private_garden(CulturalOperationWithOffsetCreate.as_view()),
         name='add_offset_co_view'),

    # Garden management
    path('<int:garden_id>/settings', access_private_garden(GardenSettings.as_view()), name='garden_settings_view'),
    path('<int:garden_id>/settings/add_user', access_private_garden(AddUserToGarden.as_view()),
         name='add_user_to_garden_view'),
    path('<int:garden_id>/settings/delete/<int:user_id>', access_private_garden(DeleteUserFromGarden.as_view()),
         name='delete_user_from_garden'),
    path('<int:garden_id>/settings/notification_delay', access_private_garden(EditNotificationDelay.as_view()),
         name='edit_notification_delay'),
    path('<int:garden_id>/settings/edit_email', access_private_garden(UserEmail.as_view()),
         name='edit_user_email'),
    path('<int:garden_id>/settings/edit_details', access_private_garden(GardenDetails.as_view()),
         name='garden_edit_details'),
    path('<int:garden_id>/settings/edit_password', access_private_garden(ChangePasswordView.as_view()),
         name='garden_edit_password'),

    # Export pages
    path('<int:garden_id>/export', access_private_garden(ExportGardenHistoryView.as_view()),
         name='garden_export_view'),
    path('<int:garden_id>/export_history', access_private_garden(ExportGardenOperationHistory.as_view()),
         name='garden_history_export_view'),
    path('<int:garden_id>/export_harvest', access_private_garden(ExportGardenHarvests.as_view()),
         name='garden_harvest_export_view'),

    # Statistics page
    path('<int:garden_id>/statistics', access_private_garden(GardenStatisticsView.as_view()),
         name='garden_statistics_view'),

    # Import from library view
    path('<int:garden_id>/import_vegetables', access_private_garden(ImportVegetablesView.as_view()),
         name='garden_import_vegetables_view'),
    path('<int:garden_id>/import_vegetables/select', access_private_garden(SelectVegetablesToImportView.as_view()),
         name='select_vegetables_to_import_view'),

    # Contact modal
    path('contact', ContactView.as_view(), name='contact_info'),

]
