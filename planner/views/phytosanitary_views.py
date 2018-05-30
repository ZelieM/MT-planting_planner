from datetime import date

from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView

from planner.forms import CustomDateInput
from planner.models import IncomingPhytosanitaire, Garden, PhytosanitaireUsage, CultivatedArea


class PhytosanitaryView(TemplateView):
    template_name = 'planner/phytosanitary_view.html'

    def get(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        incoming_register = IncomingPhytosanitaire.objects.filter(garden_id=garden_id).order_by('-receipt_date')
        usage_register = PhytosanitaireUsage.objects.filter(garden_id=garden_id).order_by('-usage_date')
        context = {'incoming_register': incoming_register, 'usage_register': usage_register}
        return render(request, self.template_name, context)


class CreatePhytosanitaryView(CreateView):
    model = IncomingPhytosanitaire
    fields = ['commercial_name', 'quantity', 'unity', 'receipt_date', 'supplier']
    template_name = 'planner/modals/incoming_phytosanitaire_create_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:phytosanitary_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def form_valid(self, form):
        new_register_entry = form.save(commit=False)
        new_register_entry.garden = Garden.objects.get(pk=self.kwargs["garden_id"])
        new_register_entry.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(CreatePhytosanitaryView, self).get_form(form_class)
        form.fields['receipt_date'].widget = CustomDateInput()
        form.fields['receipt_date'].initial = date.today()
        return form


class UpdatePhytosanitaryView(UpdateView):
    model = IncomingPhytosanitaire
    fields = ['commercial_name', 'quantity', 'unity', 'receipt_date', 'supplier']
    template_name = 'planner/modals/incoming_phytosanitaire_update_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:phytosanitary_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def get_form(self, form_class=None):
        form = super(UpdatePhytosanitaryView, self).get_form(form_class)
        form.fields['receipt_date'].widget = CustomDateInput()
        return form


class DeletePhytosanitaryView(DeleteView):
    model = IncomingPhytosanitaire
    fields = ['commercial_name', 'quantity', 'unity', 'receipt_date', 'supplier']
    template_name = 'planner/modals/incoming_phytosanitaire_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('planner:phytosanitary_view', kwargs={'garden_id': self.kwargs['garden_id']})


class CreatePhytosanitaryUsage(CreateView):
    model = PhytosanitaireUsage
    fields = ['commercial_name', 'usage_date', 'dose_used', 'unity', 'crop_treated', 'comment']
    template_name = 'planner/modals/phytosanitaire_create_usage_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:phytosanitary_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def form_valid(self, form):
        new_register_entry = form.save(commit=False)
        new_register_entry.garden = Garden.objects.get(pk=self.kwargs["garden_id"])
        new_register_entry.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super(CreatePhytosanitaryUsage, self).get_form(form_class)
        form.fields['usage_date'].widget = CustomDateInput()
        form.fields['usage_date'].initial = date.today()
        form.fields['crop_treated'].queryset = CultivatedArea.objects.filter(garden_id=self.kwargs['garden_id'])
        return form


class UpdatePhytosanitaryUsage(UpdateView):
    model = PhytosanitaireUsage
    fields = ['commercial_name', 'usage_date', 'dose_used', 'unity', 'crop_treated', 'comment']
    template_name = 'planner/modals/phytosanitaire_update_usage_form.html'

    def get_success_url(self):
        return reverse_lazy('planner:phytosanitary_view', kwargs={'garden_id': self.kwargs['garden_id']})

    def get_form(self, form_class=None):
        form = super(UpdatePhytosanitaryUsage, self).get_form(form_class)
        form.fields['usage_date'].widget = CustomDateInput()
        form.fields['crop_treated'].queryset = CultivatedArea.objects.filter(garden_id=self.kwargs['garden_id'])
        return form


class DeletePhytosanitaryUsage(DeleteView):
    model = PhytosanitaireUsage
    fields = ['commercial_name', 'usage_date', 'dose_used', 'unity', 'crop_treated', 'comment']
    template_name = 'planner/modals/phytosanitaire_usage_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('planner:phytosanitary_view', kwargs={'garden_id': self.kwargs['garden_id']})
