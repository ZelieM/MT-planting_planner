from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from planner.models import Garden, Bed


class GardenView(TemplateView):
    template_name = 'planner/bed_list.html'

    def get(self, request, *args, **kwargs):
        garden = get_object_or_404(Garden, pk=kwargs['garden_id'])
        surfaces = garden.bed_set.all()
        beds = []
        for s in surfaces:
            if isinstance(s, Bed):
                beds.append(s)
        c = {'beds': beds}
        return render(request, self.template_name, context=c)


class BedCreateView(CreateView):
    model = Bed
    fields = ['name', 'length', 'width', 'comment', 'soil_type', 'exposition']
    template_name = 'planner/modals/bed_create_with_details_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})

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


class BedDelete(DeleteView):
    model = Bed
    template_name = 'planner/modals/bed_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('planner:garden_view', kwargs={'garden_id': self.kwargs['garden_id']})
