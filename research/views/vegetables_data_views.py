from datetime import date

from django.views import View
from django.views.generic import TemplateView

from planner.import_vegetables_helpers import get_csv_writer


class VegetablesView(TemplateView):
    template_name = 'research/vegetables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from planner.models import Vegetable as gardens_vegetables
        vegetables = gardens_vegetables.objects.filter(garden__activity_data_available_for_research=True)
        context['vegetables'] = vegetables
        from vegetables_library.models import Variety as library_vegetables
        library_vegetables = library_vegetables.objects.all()
        context['library_vegetables'] = library_vegetables
        return context


class ExportVegetablesData(View):
    def get(self, request, **kwargs):
        return export_vegetables_data()


def export_vegetables_data():
    filename = "donnees_legumes_jardins_{}.csv".format(str(date.today()))
    writer, response = get_csv_writer(filename)
    from planner.models import Vegetable as gardens_vegetables
    from planner.models import CulturalOperation as gardens_operations
    vegetables = gardens_vegetables.objects.filter(garden__activity_data_available_for_research=True)
    operations = gardens_operations.objects.select_subclasses().filter(vegetable__in=vegetables)
    writer.writerow(
        ['Jardin', 'Jardin id', 'Espèce', 'Variété', 'Opération à faire', 'Id de opération', 'Date de réalisation',
         'Offset (jours)',
         'Opération précédente', 'Id opération précédente'])

    from planner.models import COWithDate as gardens_cowithdate
    for h in operations:
        if isinstance(h, gardens_cowithdate):
            writer.writerow(
                [h.vegetable.garden.name, h.vegetable.garden_id, h.vegetable.name, h.vegetable.variety, h.name, h.id,
                 h.get_date().strftime('%d-%m'), '', '', ''])
        else:
            writer.writerow(
                [h.vegetable.garden.name, h.vegetable.garden_id, h.vegetable.name, h.vegetable.variety, h.name,
                 h.id, h.get_date().strftime('%d-%m'), h.offset_in_days, h.previous_operation.name, h.previous_operation.id])
    return response
