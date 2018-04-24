import codecs
import csv
from datetime import date

from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from vegetables_library.models import Variety, CulturalOperation, COWithDate, Species


class LibraryView(TemplateView):
    template_name = 'research/library_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        species = Species.objects.all()
        context['library_species'] = species
        return context


class ExportLibrary(View):
    def get(self, request, **kwargs):
        return export_library_data()


def export_library_data():
    library_vegetables = Variety.objects.all()

    response = HttpResponse(content_type='text/csv')
    filename = "vegetable_library_data_{}.csv".format(str(date.today()))
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=';', dialect='excel', quoting=csv.QUOTE_ALL)
    writer.writerow(
        ['Légume', 'Variété', 'Operation', 'Date', 'Delai', 'Operation précédente'])
    for h in library_vegetables:
        for co in CulturalOperation.objects.select_subclasses().filter(vegetable=h):
            if isinstance(co, COWithDate):
                writer.writerow([h.name, h.variety, co.name, co.get_date(), "", ""])
            else:
                writer.writerow([h.name, h.variety, co.name, "", co.offset_in_days, co.previous_operation.name])
    return response
