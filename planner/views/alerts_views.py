from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView

from planner import queries, services, generate_pdf_helper
from planner.custom_decorators import custom_login_required
from planner.forms import ForthcomingOperationsDelayForm
from planner.models import Garden, Vegetable, Bed, ForthcomingOperation


class AlertView(TemplateView):
    template_name = 'planner/alerts.html'

    def get(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        alerts = queries.get_currently_active_alerts(garden_id)
        history = queries.done_alerts(garden_id)
        context = {'garden': Garden.objects.get(pk=garden_id), 'alerts': alerts, 'history': history}
        return render(request, self.template_name, context)


class AddSeed(View):
    """ GET : This class renders a form to add a plantation to the current garden
        POST: this class add a vegetable plantation on a specific surface of the garden"""

    def get(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        vegetables = Vegetable.objects.filter(garden_id=garden_id)
        surfaces = Bed.objects.filter(garden_id=garden_id)
        context = {'garden': Garden.objects.get(pk=garden_id), 'vegetables': vegetables, 'surfaces': surfaces}
        return render(request, 'planner/modals/add_seeding_form.html', context)

    def post(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        surface = request.POST['surface_selection']
        vegetable_id = request.POST['vegetable_selection']
        vegetable_concerned = Vegetable.objects.get(pk=vegetable_id).name
        garden = Garden.objects.get(pk=garden_id)
        if services.add_new_plantation_to_alerts(garden=garden, vegetable_id=vegetable_id, label=request.POST['seeding_label'],
                                                 surface_id=surface):
            success_message = 'Vous ({}) avez ajouté une plantation de {} '.format(
                request.user.username, vegetable_concerned)
            messages.add_message(request, messages.SUCCESS, success_message)
        else:
            warning_message = 'Cette planche a déjà une plantation de {} active, avec le même label '.format(
                vegetable_concerned)
            messages.add_message(request, messages.WARNING, warning_message)

        return HttpResponseRedirect(reverse('planner:alerts_view', kwargs={'garden_id': garden_id}))


class OperationsOnAlertViews(View):
    def get(self, request, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        context = {'garden': garden, 'alert_id': kwargs['alert_id']}
        return render(request, self.template_name, context)

class ValidateAlert(OperationsOnAlertViews):
    template_name = 'planner/modals/validate_alert_form.html'

    def post(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        alert_id = kwargs['alert_id']
        executor = request.user
        execution_date = request.POST['execution_date']
        note = request.POST['validation_note']
        duration = request.POST['duration']
        services.mark_operation_as_done(operation_id=alert_id, execution_date=execution_date, executor=executor, note=note, duration=duration)
        alert_name = ForthcomingOperation.objects.get(pk=alert_id)
        success_message = 'Vous ({}) avez indiqué avoir effectué l\'opération \" {} \" le {}'.format(
            request.user.username, alert_name, execution_date)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:alerts_view', kwargs={'garden_id': garden_id}))


class PostponeAlert(OperationsOnAlertViews):
    template_name = 'planner/modals/postpone_alert_form.html'

    def post(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        alert_id = kwargs['alert_id']
        postponement = request.POST['postponement_in_days']
        services.postpone_alert(alert_id, postponement)
        alert_name = ForthcomingOperation.objects.get(pk=alert_id)
        success_message = 'Vous avez bien reporté l\'opération \" {} \" de {} jours'.format(alert_name, postponement)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:alerts_view', kwargs={'garden_id': garden_id}))


class DeleteAlert(OperationsOnAlertViews):
    template_name = 'planner/modals/delete_alert_form.html'

    def post(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        alert_id = kwargs['alert_id']
        reason = request.POST['deletion_justification']
        note = request.POST['note']
        executor = request.user
        services.delete_operation_with_reason(alert_id, executor, reason, note)
        alert_name = ForthcomingOperation.objects.get(pk=alert_id)
        success_message = 'Vous ({}) avez supprimé l\'opération \" {} \"'.format(request.user.username, alert_name)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:alerts_view', kwargs={'garden_id': garden_id}))


class PrintForthcomingOperations(FormView):
    template_name = 'planner/modals/choose_period_to_print.html'
    form_class = ForthcomingOperationsDelayForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        context = {'garden': garden, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        garden_id = kwargs['garden_id']
        days_period = request.POST['delay_to_print']
        int_period = int(days_period)
        operations_to_print = queries.get_alert_within_notification_period(garden_id, int_period)
        return generate_pdf_helper.forthcoming_operations_as_pdf(request, operations_to_print, garden_id)

