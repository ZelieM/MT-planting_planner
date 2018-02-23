from django.contrib.auth.models import User
from django.forms import ModelForm, forms, DateField, DateInput
from .models import Garden, COWithDate, COWithOffset
from django.utils.translation import gettext_lazy as _

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
        fields = ['name', 'vegetable', 'absoluteDate', 'duration']
        widgets = {
            'absoluteDate': DateInput(),
        }


class COOffsetForm(ModelForm):
    class Meta:
        model = COWithOffset
        fields = ['name', 'vegetable', 'previous_operation', 'offset_in_days', 'duration']

