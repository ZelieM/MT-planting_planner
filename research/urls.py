from django.urls import path

from research import views
from research.custom_decorators import researcher_permission_required
from research.views import GardensView, VegetablesView, ExportGardens, LibraryView, ExportLibrary

app_name = 'research'

urlpatterns = [
    path('', researcher_permission_required()(GardensView.as_view()), name='all_gardens_view'),
    path('export_gardens', researcher_permission_required()(ExportGardens.as_view()), name='export_gardens_data'),
    path('vegetables', researcher_permission_required()(VegetablesView.as_view()), name='all_vegetables_view'),

    path('library', researcher_permission_required()(LibraryView.as_view()), name='vegetables_library_view'),
    path('export_library', researcher_permission_required()(ExportLibrary.as_view()), name='export_library'),
    path('logout', views.log_out, name="log_out"),
]
