from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.generic.base import View

from planner import services
from planner.custom_decorators import custom_login_required
from planner.forms import CustomDateInput, CustomTimeInput, CODateForm, COOffsetForm
from planner.models import Garden, COWithDate, COWithOffset, CulturalOperation


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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CulturalOperationCreate, self).get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        return context


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


class EditCulturalOperationView(View):
    template_name = 'planner/modals/edit_co_form.html'

    def get(self, request, **kwargs):
        co = CulturalOperation.objects.select_subclasses().get(pk=kwargs['co_id'])
        if isinstance(co, COWithDate):
            form = CODateForm(instance=co)
        else:
            form = COOffsetForm(instance=co)
        context = {'form': form, 'garden': Garden.objects.get(pk=kwargs['garden_id'])}
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


@custom_login_required
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


@custom_login_required
def delete_co(request, co_id):
    CulturalOperation.objects.select_subclasses().get(pk=co_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
