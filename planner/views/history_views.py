from .generic_views_overwritten import AddHistoryItemView
from planner.forms import OperationForm, ObservationForm


class AddPunctualOperationView(AddHistoryItemView):
    template_name = 'planner/modals/add_punctual_operation_form.html'
    form_class = OperationForm


class AddObservationView(AddHistoryItemView):
    template_name = 'planner/modals/add_observation_form.html'
    form_class = ObservationForm
