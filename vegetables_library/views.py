from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, CreateView

from vegetables_library.forms import VegetableForm, CustomTimeInput, CustomDateInput, CODateForm, COOffsetForm
from vegetables_library.models import Vegetable, CulturalOperation, COWithOffset, COWithDate


def index(request):
    vegetables = Vegetable.objects.values()
    cultural_operations = CulturalOperation.objects.select_subclasses()
    context = {'vegetables': vegetables, "cultural_operations": cultural_operations}
    return render(request, 'vegetables_library/vegetables_list.html', context=context)


class AddVegetableView(FormView):
    template_name = 'vegetables_library/modals/add_vegetable_to_library_form.html'
    form_class = VegetableForm

    def get(self, request, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse_lazy('vegetables_library:index', kwargs=self.kwargs)

    def form_valid(self, form):
        new_vege = form.save()
        return super().form_valid(form)


class CulturalOperationCreate(CreateView):
    template_name = "vegetables_library/create_co_form.html"

    def form_valid(self, form):
        response = super(CulturalOperationCreate, self).form_valid(form)
        return response

    def get_initial(self):
        return {'vegetable': self.kwargs['vegetable_id']}

    def get_success_url(self):
        return reverse_lazy('vegetables_library:index')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CulturalOperationCreate, self).get_context_data(**kwargs)
        return context


class CulturalOperationWithDateCreate(CulturalOperationCreate):
    template_name = "vegetables_library/create_co_form.html"
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
    template_name = "vegetables_library/create_co_form.html"
    model = COWithOffset
    fields = ['name', 'vegetable', 'previous_operation', 'offset_in_days', 'duration']


class EditCulturalOperationView(View):
    template_name = 'vegetables_library/modals/edit_co_form.html'

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
            success_message = 'L\'opération \" {} \" a bien été modifiée'.format(co.name)
            messages.add_message(request, messages.SUCCESS, success_message)
            return HttpResponseRedirect(reverse('vegetables_library:index'))


class PickCOTypeView(View):
    template_name = 'vegetables_library/modals/pick_co_type_form.html'

    def get(self, request, **kwargs):
        context = {'vegetable': kwargs['vegetable_id']}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        if request.POST['cotype'] == 'offsetco':
            return HttpResponseRedirect(reverse('vegetables_library:add_offset_co_view', kwargs=kwargs))
        else:
            return HttpResponseRedirect(reverse('vegetables_library:add_date_co_view', kwargs=kwargs))


class DeleteCOView(View):
    def get(self, request, **kwargs):
        CulturalOperation.objects.select_subclasses().get(pk=kwargs['co_id']).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
