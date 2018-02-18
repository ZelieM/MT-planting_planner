from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView
from model_utils.managers import InheritanceManager
from planner.forms import GardenForm, CODateForm, COOffsetForm, COForm
from .models import Garden, Surface, Bed, ProductionPeriod, Vegetable, CulturalOperation, COWithOffset, COWithDate

from django.contrib.auth import logout
from datetime import datetime


class CulturalOperationCreate(CreateView):

    template_name = "planner/co_form.html"
    model = CulturalOperation
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CulturalOperationCreate, self).get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        return context


def index(request):
    if request.user.is_authenticated:
        form = GardenForm()
        return HttpResponseRedirect('garden_selection', {'form': form})
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

    return render(request, 'planner/garden_selection.html', {'form': form})


@login_required(login_url="/planner/login/")
def alerts_view(request, garden_id):
    return render(request, 'planner/alertsview.html', {'garden': Garden.objects.get(pk=garden_id)})


@login_required(login_url="/planner/login/")
def garden_view(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id)
    if not ProductionPeriod.objects.filter(garden_id=garden_id):
        # If this garden doesn't have an active production period, create a new one starting now
        ProductionPeriod.objects.create(label="first_period", start_date=datetime.today(), garden_id=garden_id)
    # Take the latest production period of this garden, supposed still active
    current_period = ProductionPeriod.objects.filter(garden_id=garden_id).latest('start_date')
    surfaces = garden.surface_set.all().select_subclasses()
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
    Bed.objects.create(name=bname, length=blength, width=bwidth, garden_id=gardenid)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/planner/login/")
def delete_bed(request, bedid):
    Surface.objects.get(pk=bedid).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/planner/login/")
def vegetables_view(request, garden_id):
    garden = Garden.objects.get(pk=garden_id)
    vegetables = Vegetable.objects.values()
    # print(Vegetable.objects.get(pk=2).culturaloperation_set.all())
    cultural_operations = CulturalOperation.objects.select_subclasses()
    context = {'garden': garden, 'vegetables': vegetables, "cultural_operations": cultural_operations}
    return render(request, 'planner/my_vegetables.html', context=context)


@login_required(login_url="/planner/login/")
def edit_co_view(request, garden_id, co_id):
    # if this is a POST request we need to process the form data
    print("--------Je suis dans la view co")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        co = CulturalOperation.objects.select_subclasses().get(pk=co_id)
        if isinstance(co, COWithDate):
            form = CODateForm(request.POST, instance=co)
        else:
            form = COOffsetForm(request.POST, instance=co)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return render(request, 'planner/co_form_success.html', {'co' : co})
    # if a GET (or any other method) we'll create a blank form
    else:
        co = CulturalOperation.objects.select_subclasses().get(pk=co_id)
        if isinstance(co, COWithDate):
            form = CODateForm(instance=co)
        else:
            form = COOffsetForm(instance=co)

    return render(request, 'planner/co_form.html', {'form': form, 'garden': Garden.objects.get(pk=garden_id)})


def delete_co(request, co_id):
    CulturalOperation.objects.select_subclasses().get(pk=co_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/planner/login/")
def add_co(request, garden_id, vegetable_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = COForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/planner/%i/vegetables' % garden_id)
    # if a GET (or any other method) we'll create a blank form
    else:
            form = COForm(initial={'vegetable_id':vegetable_id})
    return render(request, 'planner/co_form.html', {'form': form, 'garden': Garden.objects.get(pk=garden_id)})


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/planner/login/")

