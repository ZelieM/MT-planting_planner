from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Garden, Bed


def index(request):
    return render(request, 'planner/index.html')


def create_garden(request):
    new_garden_name = request.POST['gardenname']
    garden = Garden.objects.create(name=new_garden_name)
    nextpage = garden.get_absolute_url()
    return HttpResponseRedirect(nextpage)


def garden_view(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id)
    beds = Bed.objects.filter(garden_id=garden.id)
    return render(request, 'planner/details.html', {'garden': garden, 'beds': beds})


def join_garden(request):
    garden = get_object_or_404(Garden, name=request.POST['gardenname'])
    nextpage = garden.get_absolute_url()
    return HttpResponseRedirect(nextpage)


def add_bed(request, gardenid):
    bname = request.POST['bedname']
    blength = request.POST['bedlength']
    bwidth = request.POST['bedwidth']
    Bed.objects.create(name=bname, length=blength, width=bwidth, garden_id=gardenid)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_bed(request, bedid):
    Bed.objects.get(pk=bedid).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def planification_view(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id)
    return render(request, 'planner/planification.html', {'garden': garden})

