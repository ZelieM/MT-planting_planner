from django.forms import widgets
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, UpdateView

from planner import services
from planner.forms import CustomDateInput, HarvestForm
from planner.models import Garden, Bed, CultivatedArea


class CropsIndexView(View):
    template_name = 'planner/crops_view.html'

    def get(self, request, **kwargs):
        garden = get_object_or_404(Garden, pk=kwargs['garden_id'])
        surfaces = garden.bed_set.all()
        beds = []
        for s in surfaces:
            if isinstance(s, Bed):
                beds.append(s)
        c = {'garden': garden, 'beds': beds}
        return render(request, self.template_name, context=c)


class DeactivateCultivatedArea(UpdateView):
    template_name = 'planner/modals/deactivate_crop_from.html'
    form_class = HarvestForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        context['area_id'] = self.kwargs['area_id']
        return context

    def get_object(self, queryset=None):
        obj = CultivatedArea.objects.get(pk=self.kwargs['area_id'])
        return obj

    def form_valid(self, form):
        form = form.save(commit=False)
        form.history = services.get_current_history(self.kwargs['garden_id'])
        form.executor = self.request.user
        form.area_concerned_id = self.kwargs['area_id']
        form.save()
        if CultivatedArea.objects.get(pk=self.kwargs['area_id']).is_active:
            services.deactivate_cultivated_area(self.kwargs['area_id'], self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('planner:crops_view', kwargs={'garden_id': self.kwargs['garden_id']})