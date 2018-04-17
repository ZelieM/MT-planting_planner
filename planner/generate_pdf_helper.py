import os
import tempfile
from html import escape
from io import BytesIO
from subprocess import Popen, PIPE

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def forthcoming_operations_as_pdf(request, operations_to_print, garden_id):
    # https://rumpelsepp.github.io/2014/09/23/generating-pdfs-with-django-and-latex.html
    context = {
        'operations': operations_to_print,
        'garden_id': garden_id,
    }
    template = get_template('planner/printable/print_operations_template.tex')
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


def render_html_template_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = context_dict
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
