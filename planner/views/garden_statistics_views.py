from django.shortcuts import render
from django.views.generic import TemplateView

from planner import compute_statistics
from planner.models import Garden


class GardenStatisticsView(TemplateView):
    template_name = 'planner/statistics_view.html'

    def get(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        x_axis_estimated, y_axis_estimated, x_axis_actual, y_axis_actual = compute_statistics.get_estimated_and_actual_work_hours_per_week(garden_id)
        context = {
                    'garden': Garden.objects.get(pk=garden_id),
                    'x_axis_estimated': x_axis_estimated,
                    'y_axis_estimated': y_axis_estimated,
                    'x_axis_actual': x_axis_actual,
                    'y_axis_actual': y_axis_actual
                    }
        return render(request, self.template_name, context)
