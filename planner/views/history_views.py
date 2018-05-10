from datetime import date

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from planner import queries, services
from planner.forms import OperationForm, ObservationForm


class AddHistoryItemView(FormView):

    def get(self, request, **kwargs):
        form = self.form_class(initial={'execution_date': date.today()})
        garden_id = kwargs['garden_id']
        form.fields["area_concerned"].queryset = queries.get_garden_areas(garden_id)
        context = {'form': form}
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse_lazy('planner:alerts_view', kwargs=self.kwargs)

    def form_valid(self, form):
        new_history_item = form.save(commit=False)
        new_history_item.executor = self.request.user
        new_history_item.history = services.get_current_history(self.kwargs['garden_id'])
        new_history_item.save()
        return super().form_valid(form)


class AddPunctualOperationView(AddHistoryItemView):
    template_name = 'planner/modals/add_punctual_operation_form.html'
    form_class = OperationForm


class AddObservationView(AddHistoryItemView):
    template_name = 'planner/modals/add_observation_form.html'
    form_class = ObservationForm
