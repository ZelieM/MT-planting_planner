from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Garden, COWithDate, COWithOffset


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class GardenForm(ModelForm):
    class Meta:
        model = Garden
        fields = ['name']


class CODateForm(ModelForm):
    class Meta:
        model = COWithDate
        fields = ['name', 'vegetable', 'duration', 'absoluteDate']


class COOffsetForm(ModelForm):
    class Meta:
        model = COWithOffset
        fields = ['name', 'vegetable', 'duration', 'offset_in_days', 'previous_operation']
