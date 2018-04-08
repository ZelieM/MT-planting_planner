from django.urls import path

from research import views
from research.custom_decorators import researcher_permission_required
from research.views import GardensView, VegetablesView, ExportGardens

app_name = 'research'

urlpatterns = [
    path('', researcher_permission_required()(GardensView.as_view()), name='all_gardens_view'),
    path('export_gardens', researcher_permission_required()(ExportGardens.as_view()), name='export_gardens_data'),
    path('/vegetables', researcher_permission_required()(VegetablesView.as_view()), name='all_vegetables_view'),
    path('logout', views.log_out, name="log_out"),
]
