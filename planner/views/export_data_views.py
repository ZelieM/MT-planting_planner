from datetime import datetime

from django.shortcuts import render
from django.views.generic import FormView

from planner import services
from planner.forms import ExportParametersForm
from planner.import_vegetables_helpers import get_csv_writer
from planner.models import CultivatedArea, IncomingPhytosanitaire, PhytosanitaireUsage


class ExportGardenHistoryView(FormView):
    template_name = 'planner/export_view.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name)


class ExportDataViews(FormView):
    template_name = 'planner/modals/export_history_dates.html'
    form_class = ExportParametersForm


class ExportGardenOperationHistory(ExportDataViews):

    def post(self, request, *args, **kwargs):
        start_date = request.POST['first_date']
        end_date = request.POST['end_date']
        return export_garden_history(first_date=start_date, end_date=end_date, garden_id=kwargs['garden_id'])


class ExportGardenHarvests(ExportDataViews):

    def post(self, request, *args, **kwargs):
        start_date = request.POST['first_date']
        end_date = request.POST['end_date']
        return export_garden_harvest_history(kwargs['garden_id'], start_date, end_date=end_date)


class ExportGardenEntryRegister(ExportDataViews):

    def post(self, request, *args, **kwargs):
        start_date = request.POST['first_date']
        end_date = request.POST['end_date']
        return export_garden_incoming_phytosanitaires(kwargs['garden_id'], start_date, end_date=end_date)


class ExportGardenUsageRegister(ExportDataViews):

    def post(self, request, *args, **kwargs):
        start_date = request.POST['first_date']
        end_date = request.POST['end_date']
        return export_garden_phytosanitary_usages(kwargs['garden_id'], start_date, end_date=end_date)


def export_garden_history(garden_id, first_date, end_date):
    first_date = datetime.strptime(first_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    history = services.get_current_history(garden_id)
    items = services.get_history_operations(history.id)
    filename = "history_from_{}.csv".format(str(first_date))
    writer, response = get_csv_writer(filename)
    writer.writerow(['Date', 'Utilisateur', 'Nom de l\'operation', 'Légume', 'Durée', 'Note'])
    for h in items:
        if first_date <= h.execution_date <= end_date:
            writer.writerow(
                [h.execution_date, h.executor.username, h.name, h.area_concerned.vegetable, h.duration, h.note])
    return response


def export_garden_harvest_history(garden_id, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    items = CultivatedArea.objects.filter(garden_id=garden_id, is_active=False)
    filename = "harvest_history_from_{}.csv".format(str(start_date))
    writer, response = get_csv_writer(filename)
    writer.writerow(['Date', 'Légume', 'Surface', 'KG', 'Revenu (€)', 'Rendement (€/kg)'])
    for h in items:
        if h.harvest_date and start_date <= h.harvest_date <= end_date:
            productivity = 0
            if h.kg_produced:
                productivity = round(h.total_selling_price / h.kg_produced, 2)
            writer.writerow(
                [h.harvest_date, h.vegetable, h.surface.name, h.kg_produced, h.total_selling_price, productivity]
            )
    return response


def export_garden_incoming_phytosanitaires(garden_id, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    items = IncomingPhytosanitaire.objects.filter(garden_id=garden_id)
    filename = "registre_entree_phytopharmaceutique_{}.csv".format(str(start_date))
    writer, response = get_csv_writer(filename)
    writer.writerow(['Nom commercial du produit', 'Quantité', 'Unité', 'Date de réception',
                     'Identification de l\'unité fournissant le produit'])
    for h in items:
        if start_date <= h.receipt_date <= end_date:
            writer.writerow(
                [h.commercial_name, h.quantity, h.unity, h.receipt_date, h.supplier]
            )
    return response


def export_garden_phytosanitary_usages(garden_id, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    items = PhytosanitaireUsage.objects.filter(garden_id=garden_id)
    filename = "registre_utilisation_phytopharmaceutique_{}.csv".format(str(start_date))
    writer, response = get_csv_writer(filename)
    writer.writerow(['Nom commercial du produit', 'Dose utilisée', 'Unité', 'Date d\'application', 'Culture traitée',
                     'Localisation de la culture', 'Surface traitée (m²)'])
    for h in items:
        if start_date <= h.usage_date <= end_date:
            writer.writerow(
                [h.commercial_name, h.dose_used, h.unity, h.usage_date, h.crop_treated.vegetable,
                 h.crop_treated.surface.name, h.crop_treated.surface.get_area]
            )
    return response
