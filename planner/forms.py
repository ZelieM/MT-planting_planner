from django.contrib.auth.models import User
from django.forms import ModelForm, forms, DateInput, TimeInput
from .models import Garden, COWithDate, COWithOffset, Operation, Observation


class CustomDateInput(DateInput):
    """ Class overwriting the DateInput class of django.forms to change the input type of DateFields to date """
    input_type = 'date'


class CustomTimeInput(TimeInput):
    """ Class overwriting the TimeInput class of django.forms to change the input type of DurationField to time """
    input_type = 'time'


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
            'absoluteDate': CustomDateInput(),
            # Show seconds for duration input field
            # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/time#Using_the_step_attribute
            'duration': CustomTimeInput(attrs={'step': 1}),
        }


class COOffsetForm(ModelForm):
    """ Model form based for the Cultural Operation with offset model """
    class Meta:
        model = COWithOffset
        fields = ['name', 'vegetable', 'previous_operation', 'offset_in_days', 'duration']


class OperationForm(ModelForm):
    class Meta:
        model = Operation
        fields = ['execution_date', 'area_concerned', 'name', 'duration', 'note']
        widgets = {
            'execution_date': CustomDateInput(),
        }


class ObservationForm(ModelForm):
    class Meta:
        model = Observation
        fields = ['execution_date', 'area_concerned', 'description']
        widgets = {
            'execution_date': CustomDateInput(),
        }
