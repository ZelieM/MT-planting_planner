from datetime import datetime, date

from django.shortcuts import render
from django.views.generic import FormView

from planner import services
from planner.forms import ExportParametersForm
from planner.import_vegetables_helpers import get_csv_writer
from planner.models import Garden, CultivatedArea


class ExportGardenHistoryView(FormView):
    template_name = 'planner/export_view.html'
    form_class = ExportParametersForm

    def get(self, request, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        form = self.form_class()
        context = {'garden': garden, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return export_garden_history(request.POST['first_date'], kwargs['garden_id'])


class ExportGardenHarvests(FormView):
    def get(self, request, *args, **kwargs):
        return export_garden_harvest_history(kwargs['garden_id'])


def export_garden_history(first_date, garden_id):
    first_date = datetime.strptime(first_date, '%Y-%m-%d').date()
    history = services.get_current_history(garden_id)
    items = services.get_history_operations(history.id)
    filename = "history_from_{}.csv".format(str(first_date))
    writer, response = get_csv_writer(filename)
    writer.writerow(['Date', 'Utilisateur', 'Nom de l\'operation', 'Légume', 'Durée', 'Note'])
    for h in items:
        if h.execution_date >= first_date:
            writer.writerow(
                [h.execution_date, h.executor.username, h.name, h.area_concerned.vegetable, h.duration, h.note])
    return response


def export_garden_harvest_history(garden_id, year=date.today().year):
    items = CultivatedArea.objects.filter(garden_id=garden_id, is_active=False, harvest_date__year=year)
    filename = "history_from_{}.csv".format(str(year))
    writer, response = get_csv_writer(filename)
    writer.writerow(['Date', 'Légume', 'Surface', 'KG', 'Revenu (€)', 'Rendement (€/kg)'])
    for h in items:
        productivity = round(h.total_selling_price / h.kg_produced, 2)
        writer.writerow(
            [h.harvest_date, h.vegetable, h.surface.name, h.kg_produced, h.total_selling_price, productivity]
        )
    return response
