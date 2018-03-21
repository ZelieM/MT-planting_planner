from django.shortcuts import render
from django.views.generic import TemplateView

from planner import compute_statistics
from planner.models import Garden


class GardenStatisticsView(TemplateView):
    template_name = 'planner/statistics_view.html'

    def get(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        data = compute_statistics.get_future_work_hours_by_week(garden_id)
        context = {'garden': Garden.objects.get(pk=garden_id), 'data': data}
        return render(request, self.template_name, context)
