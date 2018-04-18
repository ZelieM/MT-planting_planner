from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from planner.custom_decorators import custom_login_required
from planner.forms import GardenForm
from planner.models import Garden


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
            user = User.objects.create_user(username=username, password=password, email=mail)
            login(request, user)
            return HttpResponseRedirect('garden_selection')
        except IntegrityError:
            messages.error(request, 'Le nom d\'utilisateur existe deja')
            return render(request, 'planner/signup.html')

    else:
        return render(request, 'planner/signup.html')


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login/")


class GardenSelectionView(View):
    template_name = 'planner/garden_selection.html'
    form_class = GardenForm

    def get(self, request):
        form = self.form_class()
        gardens_followed = Garden.objects.filter(users=request.user)
        is_searcher = request.user.has_perm('is_researcher')
        context = {'form': form, 'gardens_followed': gardens_followed, 'is_searcher': is_searcher}
        return render(request, self.template_name, context)

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = self.form_class(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_garden = form.save(commit=False)
            new_garden.reference_email = request.user.email
            new_garden.save()
            new_garden.users.add(request.user)
            nextpage = new_garden.get_absolute_url()
            return HttpResponseRedirect(nextpage)
