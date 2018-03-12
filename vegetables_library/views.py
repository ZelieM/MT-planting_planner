from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render

from vegetables_library.models import Vegetable, CulturalOperation


def index(request):
    vegetables = Vegetable.objects.values()
    cultural_operations = CulturalOperation.objects.select_subclasses()
    context = {'vegetables': vegetables, "cultural_operations": cultural_operations}
    return render(request, 'vegetables_library/vegetables_list.html', context=context)


@login_required(login_url="/planner/login/")
def vegetables_view(request, garden_id):
    # garden = Garden.objects.get(pk=garden_id)
    vegetables = Vegetable.objects.values()
    cultural_operations = CulturalOperation.objects.select_subclasses()
    context = {'garden': garden, 'vegetables': vegetables, "cultural_operations": cultural_operations}
    return render(request, 'planner/vegetables_list.html', context=context)
