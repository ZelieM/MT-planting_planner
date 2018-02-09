from django.contrib.auth.models import User
from django.forms import ModelForm, forms
from .models import Garden


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class GardenForm(ModelForm):
    class Meta:
        model = Garden
        fields = ['name']
