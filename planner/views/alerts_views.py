from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from planner import queries, services
from planner.custom_decorators import custom_login_required
from planner.models import Garden, Vegetable, Bed, ForthcomingOperation


class AlertView(TemplateView):
    template_name = 'planner/alerts.html'

    def get(self, request, **kwargs):
        garden_id = kwargs['garden_id']
        alerts = queries.get_currently_active_alerts(garden_id)
        history = queries.done_alerts(garden_id)
        context = {'garden': Garden.objects.get(pk=garden_id), 'alerts': alerts, 'history': history}
        return render(request, self.template_name, context)


@custom_login_required
def add_seed(request, garden_id):
    # if this is a POST request we add the initial operation of the vegetable selected in the history
    if request.method == 'POST':
        surface = request.POST['surface_selection']
        vegetable_id = request.POST['vegetable_selection']
        # carea = CultivatedArea.objects.create(
        #     production_period=services.get_current_production_period(garden_id),
        #     vegetable_id=vegetable_id, label=request.POST['seeding_label'], surface_id=surface)
        vegetable_concerned = Vegetable.objects.get(pk=vegetable_id).name
        if services.add_new_plantation_to_alerts(production_period=services.get_current_production_period(garden_id),
                                                 vegetable_id=vegetable_id, label=request.POST['seeding_label'],
                                                 surface_id=surface):
            success_message = 'Vous ({}) avez ajouté une plantation de {} '.format(
                request.user.username, vegetable_concerned)
            messages.add_message(request, messages.SUCCESS, success_message)
        else:
            warning_message = 'Cette planche a déjà une plantation de {} active, avec le même label '.format(
                vegetable_concerned)
            messages.add_message(request, messages.WARNING, warning_message)

        return HttpResponseRedirect(reverse('planner:alerts_view', kwargs={'garden_id': garden_id}))
    vegetables = Vegetable.objects.filter(garden_id=garden_id)
    surfaces = Bed.objects.filter(garden_id=garden_id)
    context = {'garden': Garden.objects.get(pk=garden_id), 'vegetables': vegetables, 'surfaces': surfaces}
    return render(request, 'planner/modals/add_seeding_form.html', context)


@custom_login_required
def validate_alert(request, garden_id, alert_id):
    garden = Garden.objects.get(pk=garden_id)
    # if this is a POST request we have to mark the alert as done, else we show a modal to validate
    if request.method == 'POST':
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
    context = {'garden': garden, 'alert_id': alert_id}
    return render(request, 'planner/modals/validate_alert_form.html', context)


@custom_login_required
def postpone_alert(request, garden_id, alert_id):
    garden = Garden.objects.get(pk=garden_id)
    # if this is a POST request we have to postpone the alert by the number of days encoded
    if request.method == 'POST':
        postponement = request.POST['postponement_in_days']
        services.postpone_alert(alert_id, postponement)
        alert_name = ForthcomingOperation.objects.get(pk=alert_id)
        success_message = 'Vous avez bien reporté l\'opération \" {} \" de {} jours'.format(alert_name, postponement)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:alerts_view', kwargs={'garden_id': garden_id}))
    context = {'garden': garden, 'alert_id': alert_id}
    return render(request, 'planner/modals/postpone_alert_form.html', context)


@custom_login_required
def delete_alert(request, garden_id, alert_id):
    garden = Garden.objects.get(pk=garden_id)
    # if this is a POST request we have to postpone the alert by the number of days encoded
    if request.method == 'POST':
        reason = request.POST['deletion_justification']
        note = request.POST['note']
        executor = request.user
        services.delete_operation_with_reason(alert_id, executor, reason, note)
        alert_name = ForthcomingOperation.objects.get(pk=alert_id)
        success_message = 'Vous ({}) avez supprimé l\'opération \" {} \"'.format(request.user.username, alert_name)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:alerts_view', kwargs={'garden_id': garden_id}))
    context = {'garden': garden, 'alert_id': alert_id}
    return render(request, 'planner/modals/delete_alert_form.html', context)
