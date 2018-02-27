from django.contrib.auth.models import User
from django.forms import ModelForm, forms, DateField, DateInput
from .models import Garden, COWithDate, COWithOffset
from django.utils.translation import gettext_lazy as _


class DateInput(DateInput):
    """ Class overwriting the DateInput class of django.forms to change the input type of DateFields to date """
    input_type = 'date'


class UserForm(ModelForm):
    """ Model form based on the User model """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class GardenForm(ModelForm):
    """ Model form based on the Garden model """
    class Meta:
        model = Garden
        fields = ['name']


class CODateForm(ModelForm):
    """ Model form based for the Cultural Operation with dates model """
    class Meta:
        model = COWithDate
        fields = ['name', 'vegetable', 'absoluteDate', 'duration']
        widgets = {
            'absoluteDate': DateInput(),
        }


class COOffsetForm(ModelForm):
    """ Model form based for the Cultural Operation with offset model """
    class Meta:
        model = COWithOffset
        fields = ['name', 'vegetable', 'previous_operation', 'offset_in_days', 'duration']

