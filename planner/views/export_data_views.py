from datetime import datetime

from django.shortcuts import render
from django.views.generic import FormView

from planner import services
from planner.import_vegetables_helpers import get_csv_writer
from planner.models import CultivatedArea


class ExportGardenHistoryView(FormView):
    template_name = 'planner/export_view.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name)


class ExportGardenOperationHistory(FormView):
    def post(self, request, *args, **kwargs):
        return export_garden_history(first_date=request.POST['history_start_date'], garden_id=kwargs['garden_id'])


class ExportGardenHarvests(FormView):
    def post(self, request, *args, **kwargs):
        start_date = request.POST['harvest_history_start_date']
        return export_garden_harvest_history(kwargs['garden_id'], start_date)


def export_garden_history(garden_id, first_date):
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


def export_garden_harvest_history(garden_id, start_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    items = CultivatedArea.objects.filter(garden_id=garden_id, is_active=False)
    filename = "harvest_history_from_{}.csv".format(str(start_date))
    writer, response = get_csv_writer(filename)
    writer.writerow(['Date', 'Légume', 'Surface', 'KG', 'Revenu (€)', 'Rendement (€/kg)'])
    for h in items:
        if h.harvest_date and h.harvest_date >= start_date:
            productivity = round(h.total_selling_price / h.kg_produced, 2)
            writer.writerow(
                [h.harvest_date, h.vegetable, h.surface.name, h.kg_produced, h.total_selling_price, productivity]
            )
    return response
