import csv

from django.http import HttpResponse
from django.shortcuts import render

from planner import services
from planner.custom_decorators import custom_login_required
from planner.models import Garden


@custom_login_required
def garden_export(request, garden_id):
    garden = Garden.objects.get(pk=garden_id)
    return render(request, 'planner/export_view.html', {'garden': garden})


@custom_login_required
def export_garden_history(request, garden_id):
    history = services.get_current_history(garden_id)
    items = services.get_history_operations(history.id)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Utilisateur', 'Nom de l\'operation', 'Légume', 'Durée', 'Note'])
    for h in items:
        writer.writerow(
            [h.execution_date, h.executor.username, h.name, h.area_concerned.vegetable, h.duration, h.note])
    return response
