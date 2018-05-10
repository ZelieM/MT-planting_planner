from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.generic.base import View, TemplateView

from planner import services
from planner.forms import CustomDateInput, CustomTimeInput, CODateForm, COOffsetForm
from planner.models import COWithDate, COWithOffset, CulturalOperation


class CulturalOperationCreate(CreateView):
    template_name = "planner/create_co_form.html"

    def form_valid(self, form):
        response = super(CulturalOperationCreate, self).form_valid(form)
        services.add_new_operation_to_alerts(self.object)
        return response

    def get_initial(self):
        return {'vegetable': self.kwargs['vegetable_id']}

    def get_success_url(self):
        if self.kwargs:
            return reverse_lazy('planner:vegetables_view', kwargs={'garden_id': self.kwargs['garden_id']})
        else:
            return reverse_lazy('planner:garden_selection')


class CulturalOperationWithDateCreate(CulturalOperationCreate):
    template_name = "planner/create_co_form.html"
    model = COWithDate
    fields = ['name', 'vegetable', 'absoluteDate', 'duration']

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CulturalOperationWithDateCreate, self).get_form(form_class)
        form.fields['absoluteDate'].widget = CustomDateInput()
        # Show seconds for duration input field
        # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/time#Using_the_step_attribute
        form.fields['duration'].widget = CustomTimeInput(attrs={'step': 1})
        return form


class CulturalOperationWithOffsetCreate(CulturalOperationCreate):
    template_name = "planner/create_co_form.html"
    model = COWithOffset
    fields = ['name', 'vegetable', 'previous_operation', 'offset_in_days', 'duration']

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CulturalOperationWithOffsetCreate, self).get_form(form_class)
        # Ensure that the dropdown list of previous operation only contains operations from this garden
        form.fields['previous_operation'].queryset = CulturalOperation.objects.select_subclasses().filter(
            vegetable__garden_id=self.kwargs['garden_id'])
        return form


class EditCulturalOperationView(View):
    template_name = 'planner/modals/edit_co_form.html'

    def get(self, request, **kwargs):
        co = CulturalOperation.objects.select_subclasses().get(pk=kwargs['co_id'])
        if isinstance(co, COWithDate):
            form = CODateForm(instance=co)
        else:
            form = COOffsetForm(instance=co)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        # create a form instance and populate it with data from the request:
        co = CulturalOperation.objects.select_subclasses().get(pk=kwargs['co_id'])
        if isinstance(co, COWithDate):
            form = CODateForm(request.POST, instance=co)
        else:
            form = COOffsetForm(request.POST, instance=co)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return render(request, 'planner/modals/co_form_success.html', {'co': co})


class PickCOType(TemplateView):
    template_name = 'planner/modals/pick_co_type_form.html'

    def get(self, request, *args, **kwargs):
        # if a GET, we render the form to pick the type of operation
        context = {'vegetable': kwargs['v_id']}
        return render(request, 'planner/modals/pick_co_type_form.html', context)

    def post(self, request, *args, **kwargs):
        context = {'garden_id': kwargs['garden_id'], 'vegetable_id': kwargs['v_id']}
        if request.POST['cotype'] == 'offsetco':
            return HttpResponseRedirect(reverse('planner:add_offset_co_view', kwargs=context))
        else:
            return HttpResponseRedirect(reverse('planner:add_date_co_view', kwargs=context))


class CulturalOperationDelete(View):

    def get(self, request, *args, **kwargs):
        CulturalOperation.objects.select_subclasses().get(pk=kwargs['co_id']).delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
