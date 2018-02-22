from django.contrib.auth.models import User
from django.forms import ModelForm, forms, DateField, DateInput
from .models import Garden, COWithDate, COWithOffset


class DateInput(DateInput):
    input_type = 'date'


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
        widgets = {
            'absoluteDate': DateInput(),
        }


class COOffsetForm(ModelForm):
    class Meta:
        model = COWithOffset
        fields = ['name', 'vegetable', 'duration', 'offset_in_days', 'previous_operation']
