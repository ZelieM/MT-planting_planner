from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Garden


def index(request):
    return render(request, 'planner/index.html')


def create_garden(request):
    new_garden_name = request.POST['gardenname']
    garden = Garden.objects.create(name=new_garden_name)
    return redirect(garden)


def garden_view(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id)
    return render(request, 'planner/details.html', {'garden': garden})


def join_garden(request):
    garden = get_object_or_404(Garden, name=request.POST['gardenname'])
    return redirect(garden)
