from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from planner.custom_decorators import custom_login_required
from planner.models import Garden


@custom_login_required
def add_user_to_garden(request, garden_id):
    garden = Garden.objects.get(pk=garden_id)
    # if this is a POST request we add the user to the current garden
    if request.method == 'POST':
        user_to_add = request.POST['user_selection']
        garden.users.add(user_to_add)
        new_user_name = User.objects.get(pk=user_to_add).username
        success_message = 'Vous ({}) avez ajouté l\'utilisateur "{}" au jardin: " {} " '.format(
            request.user.username, new_user_name, garden.name)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:garden_settings_view', kwargs={'garden_id': garden_id}))
    users = User.objects.exclude(garden=garden)
    context = {'garden': garden, 'users': users}
    return render(request, 'planner/modals/add_user_to_garden_form.html', context)


@custom_login_required
def garden_settings(request, garden_id):
    garden = Garden.objects.get(pk=garden_id)
    following_users = garden.users.all()
    return render(request, 'planner/parameters_view.html', {'garden': garden, 'following_users': following_users})


@custom_login_required
def delete_user_from_garden(request, garden_id, user_id):
    deleted_user = User.objects.get(pk=user_id)
    garden = Garden.objects.get(pk=garden_id)
    garden.users.remove(deleted_user)
    success_message = 'Vous ({}) avez supprimé l\'utilisateur \" {} \"'.format(request.user.username, deleted_user)
    messages.add_message(request, messages.SUCCESS, success_message)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@custom_login_required
def edit_notification_delay(request, garden_id):
    garden = Garden.objects.get(pk=garden_id)
    # if this is a POST request we have to change the notification delay of this garden
    if request.method == 'POST':
        new_delay = request.POST['notification_delay']
        garden.notification_delay = new_delay
        garden.save()
        success_message = 'Les alertes apparaitront maintenant {} jours avant la date d\'échéance'.format(new_delay)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:garden_settings_view', kwargs={'garden_id': garden_id}))
    context = {'garden': garden}
    return render(request, 'planner/modals/edit_notification_delay_form.html', context)


class UserUpdate(UpdateView):
    model = User
    fields = ['email']
    template_name = 'planner/modals/user_update_email_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        return context

    def get_object(self, queryset=None):
        obj = User.objects.get(pk=self.request.user.id)
        return obj

    def get_success_url(self):
        return reverse_lazy('planner:garden_settings_view', kwargs={'garden_id': self.kwargs['garden_id']})


class GardenDetailsUpdate(UpdateView):
    model = Garden
    fields = ['name', 'comment', 'soil_type', 'culture_type', 'reference_email']
    template_name = 'planner/modals/garden_update_details_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['garden'] = Garden.objects.get(pk=self.kwargs["garden_id"])
        return context

    def get_object(self, queryset=None):
        obj = Garden.objects.get(pk=self.kwargs["garden_id"])
        return obj

    def get_success_url(self):
        return reverse_lazy('planner:garden_settings_view', kwargs={'garden_id': self.kwargs['garden_id']})
