import codecs
import csv
import os
import tempfile
from datetime import date
from subprocess import Popen, PIPE

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView

from planner.models import Garden


class GardensView(TemplateView):
    template_name = 'research/gardens.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the gardens
        gardens = Garden.objects.filter(details_available_for_research=True)
        context['gardens'] = gardens
        return context


def garden_as_pdf(request):
    # https://rumpelsepp.github.io/2014/09/23/generating-pdfs-with-django-and-latex.html
    gardens = Garden.objects.filter(details_available_for_research=True)
    context = {
        'gardens': gardens,
    }
    template = get_template('research/latex_template.tex')
    rendered_tpl = template.render(context).encode('utf-8')
    # Python3 only. For python2 check out the docs!
    with tempfile.TemporaryDirectory() as tempdir:
        # Create subprocess, supress output with PIPE and
        # run latex twice to generate the TOC properly.
        # Finally read the generated pdf.
        for i in range(2):
            process = Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(rendered_tpl)
        with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
            pdf = f.read()
    r = HttpResponse(content_type='application/pdf')
    # r['Content-Disposition'] = 'attachment; filename=texput.pdf'
    r.write(pdf)
    return r


class ExportGardens(View):

    def get(self, request, **kwargs):
        return export_gardens_data()


def export_gardens_data():
    gardens = Garden.objects.filter(details_available_for_research=True)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    filename = "gardens_data_{}.csv".format(str(date.today()))
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=';', dialect='excel', quoting=csv.QUOTE_ALL)
    writer.writerow(
        ['Nom du jardin', 'Code Postal', 'Adresse email', 'Description', 'Type de sol', 'Agriculture', 'Utilisateurs'])
    for h in gardens:
        n = len(User.objects.filter(garden=h))
        writer.writerow(
            [h.name, h.postal_code, h.reference_email, h.comment, h.soil_type, h.culture_type, n])
    return response
