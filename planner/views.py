from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages

from planner.forms import GardenForm
from .models import Garden, Surface, Bed, ProductionPeriod, Vegetable, CulturalOperation


from datetime import datetime
from .ganttchart import create_gantt


def index(request): # TODO : if user logged in, redirect to garden_selection
    return HttpResponseRedirect('login')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        mail = request.POST['mailaddress']
        try:
            User.objects.create_user(username=username, password=password, email=mail)
            return HttpResponseRedirect('garden_selection')
        except IntegrityError:
            messages.error(request, 'Le nom d\'utilisateur existe deja')
            return render(request, 'planner/signup.html')

    else:
        return render(request, 'planner/signup.html')


@login_required(login_url="/planner/login/")
def garden_selection(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GardenForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_garden = form.save()
            nextpage = new_garden.get_absolute_url()
            return HttpResponseRedirect(nextpage)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = GardenForm()

    return render(request,  'planner/gardenselection.html', {'form': form})


@login_required(login_url="/planner/login/")
def garden_view(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id)
    if not ProductionPeriod.objects.filter(garden_id=garden_id):
        # If this garden doesn't have an active production period, create a new one starting now
        ProductionPeriod.objects.create(label="first_period", start_date=datetime.today(), garden_id=garden_id)
    # Take the latest production period of this garden, supposed still active
    current_period = ProductionPeriod.objects.filter(garden_id=garden_id).latest('start_date')
    surfaces = ProductionPeriod.objects.get(pk=current_period.id).surface_set.select_subclasses()
    c = {'garden': garden, 'beds': surfaces, 'current_period': current_period}
    return render(request, 'planner/details.html', context=c)


@login_required(login_url="/planner/login/")
def join_garden(request):
    garden = get_object_or_404(Garden, name=request.POST['gardenname'])
    nextpage = garden.get_absolute_url()
    return HttpResponseRedirect(nextpage)


@login_required(login_url="/planner/login/")
def add_bed(request, gardenid):
    bname = request.POST['bedname']
    blength = request.POST['bedlength']
    bwidth = request.POST['bedwidth']
    current_period = ProductionPeriod.objects.filter(garden_id=gardenid).latest('start_date')
    Bed.objects.create(name=bname, length=blength, width=bwidth, production_period=current_period)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/planner/login/")
def delete_bed(request, bedid):
    Surface.objects.get(pk=bedid).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/planner/login/")
def vegetables_view(request, garden_id):
    garden = Garden.objects.get(pk=garden_id)
    vegetables = Vegetable.objects.values()
    print(Vegetable.objects.get(pk=2).culturaloperation_set.all())
    cultural_operations = CulturalOperation.objects.select_subclasses()
    context = {'garden': garden, 'vegetables': vegetables, "cultural_operations": cultural_operations}
    return render(request, 'planner/myvegetables.html', context=context)


# @login_required(login_url="/planner/login/")
# def planification_view(request, garden_id):
#     garden = get_object_or_404(Garden, pk=garden_id)
#     beds = Bed.objects.filter(garden_id=garden.id)
#     beds_ids = Bed.objects.filter(garden_id=garden.id).values_list('id', flat=True)
#     vegetables = Vegetable.objects.all()
#     events = Event.objects.filter(bed_id__in=beds_ids)
#     create_gantt(events, garden_id)
#     return render(request, 'planner/planification.html', {'garden': garden, 'beds': beds, 'vegetables': vegetables, 'events': events})
#
#
# @login_required(login_url="/planner/login/")
# def add_event(request):
#     vid = request.POST["vegetablename"]
#     bid = request.POST["bedname"]
#     seedingS = request.POST["seedingstart"]
#     seedingE = request.POST["seedingend"]
#     harvestS = request.POST["harveststart"]
#     harvestE = request.POST["harvestend"]
#     Event.objects.create(bed_id=bid, vegetable_id=vid, seeding_start=seedingS, seeding_end=seedingE, harvest_start=harvestS, harvest_end=harvestE)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
