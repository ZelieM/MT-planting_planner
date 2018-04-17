from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from planner.custom_decorators import custom_login_required
from planner.forms import VegetableForm
from planner.models import Garden, Vegetable, CulturalOperation


class VegetablesView(TemplateView):
    template_name = 'planner/vegetables_list.html'

    def get(self, request, *args, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        vegetables = Vegetable.objects.filter(garden=garden)
        cultural_operations = CulturalOperation.objects.select_subclasses()
        context = {'garden': garden, 'vegetables': vegetables, "cultural_operations": cultural_operations}
        return render(request, self.template_name, context=context)


class AddVegetableView(FormView):
    template_name = 'planner/modals/add_vegetable_to_garden_form.html'
    form_class = VegetableForm

    def get(self, request, **kwargs):
        form = self.form_class()
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        context = {'garden': garden, 'form': form}
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse_lazy('planner:vegetables_view', kwargs=self.kwargs)

    def form_valid(self, form):
        new_vegetable = form.save(commit=False)
        new_vegetable.garden_id = self.kwargs['garden_id']
        new_vegetable.save()
        return super().form_valid(form)
