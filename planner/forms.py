from django.contrib.auth.models import User
from django.forms import ModelForm, forms
from .models import Garden, COWithDate, COWithOffset, CulturalOperation


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class GardenForm(ModelForm):
    class Meta:
        model = Garden
        fields = ['name']


class COForm(ModelForm):
    class Meta:
        model = CulturalOperation
        fields = '__all__'


class CODateForm(ModelForm):
    class Meta:
        model = COWithDate
        fields = '__all__'


class COOffsetForm(ModelForm):
    class Meta:
        model = COWithOffset
        fields = '__all__'
