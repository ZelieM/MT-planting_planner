from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from planner import services
from planner.custom_decorators import custom_login_required
from planner.models import Garden, Bed


@custom_login_required
def garden_view(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id)
    current_period = services.get_current_production_period(garden_id)
    surfaces = garden.bed_set.all()
    beds = []
    for s in surfaces:
        if isinstance(s, Bed):
            beds.append(s)
    c = {'garden': garden, 'beds': beds, 'current_period': current_period}
    return render(request, 'planner/bed_list.html', context=c)


@custom_login_required
def add_bed(request, garden_id):
    bname = request.POST['bedname']
    blength = request.POST['bedlength']
    bwidth = request.POST['bedwidth']
    Bed.objects.create(name=bname, length=blength, width=bwidth, garden_id=garden_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@custom_login_required
def delete_bed(request, bedid):
    Bed.objects.get(pk=bedid).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BedCreateView(CreateView):
    model = Bed
    fields = ['name', 'length', 'width', 'comment', 'soil_type', 'exposition']
    template_name = 'planner/modals/bed_create_with_details_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        return context

    def form_valid(self, form):
        new_bed = form.save(commit=False)
        new_bed.garden = Garden.objects.get(pk=self.kwargs["garden_id"])
        new_bed.save()
        return super().form_valid(form)


class BedUpdateView(UpdateView):
    model = Bed
    fields = ['name', 'length', 'width', 'comment', 'soil_type', 'exposition']
    template_name = 'planner/modals/bed_update_with_details_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        return context


class BedDelete(DeleteView):
    model = Bed
    template_name = 'planner/modals/bed_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        return context

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})


