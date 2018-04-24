from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from planner import import_vegetables_helpers
from planner.models import Garden
from vegetables_library.models import CulturalOperation as library_operation
from vegetables_library.models import Variety as library_vegetable
from vegetables_library.models import Species as library_species


class ImportVegetablesView(View):
    template_name = 'planner/import_vegetables_view.html'

    def get(self, request, **kwargs):
        species_from_library = library_species.objects.all()
        operations_from_library = library_operation.objects.select_subclasses()
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        context = {'species_from_library': species_from_library,
                   'operations_from_library': operations_from_library, 'garden': garden}
        return render(request, self.template_name, context)


class SelectVegetablesToImportView(FormView):
    template_name = 'planner/modals/select_vegetables_to_import.html'

    def get(self, request, **kwargs):
        varieties_from_library = library_vegetable.objects.all()
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        context = {'varieties_from_library': varieties_from_library, 'garden': garden}
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse_lazy('planner:garden_import_vegetables_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def post(self, request, *args, **kwargs):
        vegetables_selected = request.POST.getlist('vegetables_id')
        import_vegetables_helpers.import_vegetables_to_garden(kwargs['garden_id'], vegetables_selected)
        return HttpResponseRedirect(self.get_success_url())
