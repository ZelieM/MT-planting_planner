from django.urls import path

from vegetables_library import views
from vegetables_library.views import AddVegetableView, EditCulturalOperationView, CulturalOperationWithDateCreate, \
    CulturalOperationWithOffsetCreate, PickCOTypeView, DeleteCOView

app_name = 'vegetables_library'

urlpatterns = [

    path('', views.index, name='index'),
    path('vegetables/delete_co/<int:co_id>', DeleteCOView.as_view(), name='delete_co'),
    path('add_vegetable', AddVegetableView.as_view(), name='add_vegetable_to_library_view'),
    path('co/<int:co_id>', EditCulturalOperationView.as_view(), name='edit_co_view'),
    path('pick_co/<int:vegetable_id>', PickCOTypeView.as_view(), name='pick_co_type'),
    path('<int:vegetable_id>/add_date_co', CulturalOperationWithDateCreate.as_view(), name='add_date_co_view'),
    path('<int:vegetable_id>/add_offset_co', CulturalOperationWithOffsetCreate.as_view(), name='add_offset_co_view'),

]
