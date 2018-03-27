import csv

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from planner import services

from planner.forms import ExportParametersForm
from planner.models import Garden


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


def export_garden_history(first_date, garden_id):
    first_date = datetime.strptime(first_date, '%Y-%m-%d').date()
    history = services.get_current_history(garden_id)
    items = services.get_history_operations(history.id)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    filename = "history_from_{}.csv".format(str(first_date))
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    writer = csv.writer(response)
    writer.writerow(['Date', 'Utilisateur', 'Nom de l\'operation', 'Légume', 'Durée', 'Note'])
    for h in items:
        if h.execution_date >= first_date:
            writer.writerow(
                [h.execution_date, h.executor.username, h.name, h.area_concerned.vegetable, h.duration, h.note])
    return response
