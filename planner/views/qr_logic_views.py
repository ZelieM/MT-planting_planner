from html import escape
from io import BytesIO

from django.urls import reverse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

from django.shortcuts import render
from django.views import View

from planner.models import Garden, Bed, CultivatedArea


class BedQRView(View):
    template_name = 'planner/qr_bed_view.html'

    def get(self, *args, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        bed = Bed.objects.get(pk=kwargs['pk'])
        active_areas = CultivatedArea.objects.filter(garden=garden, surface=bed, is_active=True)
        context = {'garden': garden, 'bed': bed, 'areas': active_areas}
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
        print("urls")
        print(urls)
        return render_to_pdf(
            self.template_name,
            {
                'pagesize': 'A4',
                'beds': beds,
                'urls': urls
            })


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = context_dict
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
