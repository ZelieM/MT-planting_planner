from django.http import HttpResponse
from django.shortcuts import render

from research.custom_decorators import researcher_permission_required


@researcher_permission_required()
def index(request):
    return render(request, 'research/index.html')
