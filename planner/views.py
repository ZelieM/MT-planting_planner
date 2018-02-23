from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from planner import queries, services
from planner.forms import GardenForm, CODateForm, COOffsetForm, DateInput
from .models import Garden, Surface, Bed, ProductionPeriod, Vegetable, CulturalOperation, COWithOffset, COWithDate, \
    CulturalOperationHistory, CultivatedArea, Area

from django.contrib.auth import logout


class CulturalOperationWithDateCreate(CreateView):
    template_name = "planner/create_co_form.html"
    model = COWithDate
    fields = ['name', 'vegetable', 'absoluteDate', 'duration']

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CulturalOperationWithDateCreate, self).get_form(form_class)
        form.fields['absoluteDate'].widget = DateInput()
        return form

    def get_initial(self):
        return {'vegetable': self.kwargs['vegetable_id']}

    def get_success_url(self):
        if self.kwargs:
            return reverse_lazy('planner:vegetables_view', kwargs={'garden_id': self.kwargs['garden_id']})
        else:
            return reverse_lazy('planner:garden_selection')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CulturalOperationWithDateCreate, self).get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        return context


class CulturalOperationWithOffsetCreate(CreateView):
    template_name = "planner/create_co_form.html"
    model = COWithOffset
    fields = ['name', 'vegetable', 'previous_operation', 'offset_in_days', 'duration']

    def get_initial(self):
        return {'vegetable': self.kwargs['vegetable_id']}

    def get_success_url(self):
        if self.kwargs:
            return reverse_lazy('planner:vegetables_view', kwargs={'garden_id': self.kwargs['garden_id']})
        else:
            return reverse_lazy('planner:garden_selection')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CulturalOperationWithOffsetCreate, self).get_context_data(**kwargs)
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
    alerts = queries.active_alerts(garden_id)
    history = queries.done_alerts(garden_id)
    # alerts = queries.active_alerts(garden_id)
    # history = CulturalOperationHistory.objects.filter(
    #     production_period=queries.get_current_production_period(garden_id))
    # context = {'garden': Garden.objects.get(pk=garden_id), 'alerts': alerts, 'history': history}
    context = {'garden': Garden.objects.get(pk=garden_id), 'alerts': alerts, 'history': history}
    return render(request, 'planner/alerts.html', context)


@login_required(login_url="/planner/login/")
def garden_view(request, garden_id):
    garden = get_object_or_404(Garden, pk=garden_id)
    current_period = queries.get_current_production_period(garden_id)

    surfaces = garden.surface_set.all().select_subclasses()
    c = {'garden': garden, 'beds': surfaces, 'current_period': current_period}
    return render(request, 'planner/bed_list.html', context=c)


@login_required(login_url="/planner/login/")
def join_garden(request):
    garden = get_object_or_404(Garden, name=request.POST['gardenname'])
    nextpage = garden.get_absolute_url()
    return HttpResponseRedirect(nextpage)


@login_required(login_url="/planner/login/")
def add_bed(request, garden_id):
    bname = request.POST['bedname']
    blength = request.POST['bedlength']
    bwidth = request.POST['bedwidth']
    Bed.objects.create(name=bname, length=blength, width=bwidth, garden_id=garden_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/planner/login/")
def delete_bed(request, bedid):
    Surface.objects.get(pk=bedid).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/planner/login/")
def vegetables_view(request, garden_id):
    garden = Garden.objects.get(pk=garden_id)
    vegetables = Vegetable.objects.values()
    cultural_operations = CulturalOperation.objects.select_subclasses()
    context = {'garden': garden, 'vegetables': vegetables, "cultural_operations": cultural_operations}
    return render(request, 'planner/vegetables_list.html', context=context)


@login_required(login_url="/planner/login/")
def edit_co_view(request, garden_id, co_id):
    # if this is a POST request we need to process the form data
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
            return render(request, 'planner/modals/co_form_success.html', {'co': co})
    # if a GET (or any other method) we'll create a blank form
    else:
        co = CulturalOperation.objects.select_subclasses().get(pk=co_id)
        if isinstance(co, COWithDate):
            form = CODateForm(instance=co)
        else:
            form = COOffsetForm(instance=co)

    return render(request, 'planner/modals/edit_co_form.html',
                  {'form': form, 'garden': Garden.objects.get(pk=garden_id)})


@login_required(login_url="/planner/login/")
def pick_co_type(request, garden_id, v_id):
    # if this is a POST request we need to redirect to a form to create the new operation
    if request.method == 'POST':
        urlargs = {'garden_id': garden_id, 'vegetable_id': v_id}
        if request.POST['cotype'] == 'offsetco':
            return HttpResponseRedirect(reverse('planner:add_offset_co_view', kwargs=urlargs))
        else:
            return HttpResponseRedirect(reverse('planner:add_date_co_view', kwargs=urlargs))
    # if a GET, we render the form to pick the type of operation
    context = {'garden': Garden.objects.get(pk=garden_id), 'vegetable': v_id}
    return render(request, 'planner/modals/pick_co_type_form.html', context)


def delete_co(request, co_id):
    CulturalOperation.objects.select_subclasses().get(pk=co_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/planner/login/")


@login_required(login_url="/planner/login/")
def add_seed(request, garden_id):
    # if this is a POST request we add the initial operation of the vegetable selected in the history
    if request.method == 'POST':
        # TODO create a cultivated area with the vegetable, the surface sowed and and the label
        surface = Area.objects.create(area_surface=request.POST['surface_seeded'], garden_id=garden_id)
        carea = CultivatedArea.objects.create(production_period=queries.get_current_production_period(garden_id),
                                             vegetable_id=request.POST['vegetable_selection'],
                                             label=request.POST['seeding_label'],
                                             surface=surface)
        services.add_initial_operation_to_alerts(cultivated_area=carea, date=request.POST['seedingdate'])
        #
        # services.add_initial_operation_to_history(garden_id, request.POST['vegetable_selection'],
        #                                           request.POST['seedingdate'])
        return HttpResponseRedirect(reverse('planner:alerts_view', kwargs={'garden_id': garden_id}))
    vegetables = Vegetable.objects.all()
    context = {'garden': Garden.objects.get(pk=garden_id), 'vegetables': vegetables}
    return render(request, 'planner/modals/add_seeding_form.html', context)
