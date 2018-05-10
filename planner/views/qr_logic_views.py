from django.urls import reverse
from django.views.generic import TemplateView

from django.shortcuts import render
from django.views import View

from planner import queries
from planner.generate_pdf_helper import render_html_template_to_pdf
from planner.models import Garden, Bed, CultivatedArea


class BedQRView(View):
    template_name = 'planner/qr_bed_view.html'

    def get(self, *args, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        bed = Bed.objects.get(pk=kwargs['pk'])
        active_areas = CultivatedArea.objects.filter(garden=garden, surface=bed, is_active=True)
        context = {'bed': bed, 'areas': active_areas}
        return render(self.request, self.template_name, context)


class PrintQRView(View):
    template_name = 'planner/printable/print_qr_template.html'

    def get(self, *args, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        beds = Bed.objects.filter(garden=garden)
        urls = {}
        for b in beds:
            urls[b] = self.request.build_absolute_uri(
                reverse('planner:qr_bed_view', kwargs={'garden_id': garden.id, 'pk': b.id}))
        return render_html_template_to_pdf(
            self.template_name,
            {
                'pagesize': 'A4',
                'beds': beds,
                'urls': urls
            })


class OperationByAreaQRView(TemplateView):
    template_name = 'planner/alerts_by_area.html'

    def get(self, request, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        area = CultivatedArea.objects.get(pk=kwargs['pk'])
        alerts = queries.get_currently_active_alerts(garden.id, area.id)
        context = {'alerts': alerts, 'area': area}
        return render(request, self.template_name, context)
