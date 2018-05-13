from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, TemplateView, FormView

from planner.models import Garden


class AddUserToGarden(TemplateView):
    template_name = 'planner/modals/add_user_to_garden_form.html'

    def get(self, request, *args, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        users = User.objects.exclude(garden=garden)
        context = {'garden': garden, 'users': users}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        user_to_add = request.POST['user_selection']
        garden.users.add(user_to_add)
        new_user_name = User.objects.get(pk=user_to_add).username
        success_message = 'Vous ({}) avez ajouté l\'utilisateur "{}" au jardin: " {} " '.format(
            request.user.username, new_user_name, garden.name)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:garden_settings_view', kwargs=kwargs))


class GardenSettings(TemplateView):
    template_name = 'planner/parameters_view.html'

    def get(self, request, *args, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        following_users = garden.users.all()
        context = {'garden': garden, 'following_users': following_users}
        return render(request, self.template_name, context)


class DeleteUserFromGarden(View):

    def get(self, request, *args, **kwargs):
        deleted_user = User.objects.get(pk=kwargs['user_id'])
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        garden.users.remove(deleted_user)
        success_message = 'Vous ({}) avez supprimé l\'utilisateur \" {} \"'.format(request.user.username, deleted_user)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class EditNotificationDelay(View):
    template_name = 'planner/modals/edit_notification_delay_form.html'

    def get(self, request, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        context = {'garden': garden}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        garden = Garden.objects.get(pk=kwargs['garden_id'])
        new_delay = request.POST['notification_delay']
        garden.notification_delay = new_delay
        garden.save()
        success_message = 'Les alertes apparaitront maintenant {} jours avant la date d\'échéance'.format(new_delay)
        messages.add_message(request, messages.SUCCESS, success_message)
        return HttpResponseRedirect(reverse('planner:garden_settings_view', kwargs=kwargs))


class GardenDetailsUpdate(UpdateView):

    def get_success_url(self):
        return reverse_lazy('planner:garden_settings_view', kwargs={'garden_id': self.kwargs['garden_id']})


class UserEmail(GardenDetailsUpdate):
    model = User
    fields = ['email']
    template_name = 'planner/modals/user_update_email_form.html'

    def get_object(self, queryset=None):
        obj = User.objects.get(pk=self.request.user.id)
        return obj


class GardenDetails(GardenDetailsUpdate):
    model = Garden
    fields = ['name', 'postal_code', 'comment', 'soil_type', 'culture_type', 'reference_email',
              'details_available_for_research',
              'activity_data_available_for_research']
    template_name = 'planner/modals/garden_update_details_form.html'

    def get_object(self, queryset=None):
        obj = Garden.objects.get(pk=self.kwargs["garden_id"])
        return obj


class ChangePasswordView(FormView):
    template_name = 'planner/modals/change_password.html'

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot de passe a bien été changé')
            return HttpResponseRedirect(reverse('planner:garden_settings_view', kwargs=kwargs))
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})
