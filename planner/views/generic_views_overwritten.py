from datetime import date

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView

from planner import services, queries
from planner.models import Garden


class CreateGardenDependentObjects(CreateView):

    def form_valid(self, form):
        new_object = form.save(commit=False)
        new_object.garden = Garden.objects.get(pk=self.kwargs["garden_id"])
        new_object.save()
        return super().form_valid(form)


class GardenDetailsUpdate(UpdateView):

    def get_success_url(self):
        return reverse_lazy('planner:garden_settings_view', kwargs={'garden_id': self.kwargs['garden_id']})


class OperationsOnAlertViews(View):
    def get(self, request, **kwargs):
        context = {'alert_id': kwargs['alert_id']}
        return render(request, self.template_name, context)


class CulturalOperationCreate(CreateView):
    template_name = "planner/create_co_form.html"

    def form_valid(self, form):
        response = super(CulturalOperationCreate, self).form_valid(form)
        services.add_new_operation_to_alerts(self.object)
        return response

    def get_initial(self):
        return {'vegetable': self.kwargs['vegetable_id']}

    def get_success_url(self):
        if self.kwargs:
            return reverse_lazy('planner:vegetables_view', kwargs={'garden_id': self.kwargs['garden_id']})
        else:
            return reverse_lazy('planner:garden_selection')


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