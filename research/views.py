import os
from django.http import HttpResponse
from django.shortcuts import render

from planner.models import Garden
from research.custom_decorators import researcher_permission_required

from django.template import Context
from django.template.loader import get_template
from subprocess import Popen, PIPE
import tempfile


@researcher_permission_required()
def index(request):
    gardens = Garden.objects.all()
    context = {'gardens': gardens}
    # return render(request, 'research/index.html', context)
    return garden_as_pdf(request)


def garden_as_pdf(request):
    # https://rumpelsepp.github.io/2014/09/23/generating-pdfs-with-django-and-latex.html
    gardens = Garden.objects.all()
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
