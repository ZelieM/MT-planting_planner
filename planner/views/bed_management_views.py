from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, View
from django.http import HttpResponse
import json

from planner.models import Garden, Bed, Parcel


class GardenView(TemplateView):
    template_name = 'planner/bed_list.html'

    def get(self, request, *args, **kwargs):
        garden = get_object_or_404(Garden, pk=kwargs['garden_id'])
        surfaces = garden.bed_set.all()
        beds = []
        for s in surfaces:
            if isinstance(s, Bed):
                beds.append(s)
        parcels = Parcel.objects.filter(garden_id=garden.id)
        c = {'parcels': parcels, 'beds': beds}
        return render(request, self.template_name, context=c)


class BedCreateView(CreateView):
    model = Bed
    fields = ['parcel', 'name', 'length', 'width', 'comment', 'soil_type', 'exposition']
    template_name = 'planner/modals/bed_create_with_details_form.html'

    def get_form(self, *args, **kwargs):
        form = super(BedCreateView, self).get_form(*args, **kwargs)
        form.fields['parcel'].queryset = Parcel.objects.filter(garden_id=self.kwargs['garden_id'])
        return form

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def form_valid(self, form):
        new_bed = form.save(commit=False)
        new_bed.garden = Garden.objects.get(pk=self.kwargs["garden_id"])
        new_bed.save()
        return super().form_valid(form)


class BedUpdateView(UpdateView):
    model = Bed
    fields = ['parcel', 'name', 'length', 'width', 'comment', 'soil_type', 'exposition']
    template_name = 'planner/modals/bed_update_with_details_form.html'

    def get_form(self, *args, **kwargs):
        form = super(BedUpdateView, self).get_form(*args, **kwargs)
        form.fields['parcel'].queryset = Parcel.objects.filter(garden_id=self.kwargs['garden_id'])
        return form

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})


class BedDelete(DeleteView):
    model = Bed
    template_name = 'planner/modals/bed_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})


class ParcelCreateView(CreateView):
    model = Parcel
    fields = ['name']
    template_name = 'planner/modals/parcel_create_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def form_valid(self, form):
        new_parcel = form.save(commit=False)
        new_parcel.garden = Garden.objects.get(pk=self.kwargs["garden_id"])
        new_parcel.save()
        return super().form_valid(form)


class ParcelUpdateView(UpdateView):
    model = Parcel
    fields = ['name']
    template_name = 'planner/modals/parcel_update_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})


class ParcelDelete(DeleteView):
    model = Parcel
    template_name = 'planner/modals/parcel_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})


class SaveBedPosition(View):
    def post(self, request, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        for e in json_data:
            current_bed = Bed.objects.get(pk=e.get('id'))
            current_bed.x = e.get('x')
            current_bed.y = e.get('y')
            current_bed.save()

        return HttpResponse()
