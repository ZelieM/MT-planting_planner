from datetime import date

from django.views import View
from django.views.generic import TemplateView

from planner.import_vegetables_helpers import get_csv_writer
from vegetables_library.models import Variety, CulturalOperation, COWithDate, Species


class LibraryView(TemplateView):
    template_name = 'research/library_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_varieties'] = Variety.objects.all().order_by('species__french_name')
        return context


class ExportLibraryOperations(View):
    def get(self, request, **kwargs):
        return export_library_data()


class ExportLibraryVarieties(View):
    def get(self, request, **kwargs):
        return export_library_varieties()


class ExportLibrarySpecies(View):
    def get(self, request, **kwargs):
        return export_library_species()


def export_library_varieties():
    library_vegetables = Variety.objects.all()
    filename = "vegetable_library_varieties_{}.csv".format(str(date.today()))
    (writer, response) = get_csv_writer(filename)
    writer.writerow(
        ['Espèce', 'Variété FR', 'Variété LATIN', 'Début semis', 'Fin semis', 'Début récolte', 'Fin récolte',
         'Durée du cycle', 'Note'])
    for h in library_vegetables:
        writer.writerow([h.species.french_name, h.french_name, h.latin_name, h.open_ground_seeding.seeding_start,
                         h.open_ground_seeding.seeding_end, h.open_ground_seeding.harvest_start,
                         h.open_ground_seeding.harvest_end, h.open_ground_seeding.cycle_duration, h.comment])
    return response


def export_library_species():
    library_vegetables = Species.objects.all()
    filename = "vegetable_library_species_{}.csv".format(str(date.today()))
    (writer, response) = get_csv_writer(filename)
    writer.writerow(
        ['Espèce FR', 'Espèce LATIN', 'Famille', 'Type'])
    for h in library_vegetables:
        writer.writerow([h.french_name, h.latin_name, h.family, h.vegetable_type])
    return response


def export_library_data():
    library_vegetables = Variety.objects.all()
    filename = "vegetable_library_data_{}.csv".format(str(date.today()))
    (writer, response) = get_csv_writer(filename)
    writer.writerow(
        ['Légume', 'Variété', 'Operation', 'Date', 'Delai', 'Operation précédente'])
    for h in library_vegetables:
        for co in CulturalOperation.objects.select_subclasses().filter(vegetable=h):
            if isinstance(co, COWithDate):
                writer.writerow([h.name, h.variety, co.name, co.get_date(), "", ""])
            else:
                writer.writerow([h.name, h.variety, co.name, "", co.offset_in_days, co.previous_operation.name])
    return response
