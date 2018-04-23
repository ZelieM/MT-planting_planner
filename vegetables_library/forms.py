from django.forms import ModelForm, DateInput, TimeInput

from vegetables_library.models import Variety, COWithDate, COWithOffset


class CustomDateInput(DateInput):
    """ Class overwriting the DateInput class of django.forms to change the input type of DateFields to date """
    input_type = 'date'


class CustomTimeInput(TimeInput):
    """ Class overwriting the TimeInput class of django.forms to change the input type of DurationField to time """
    input_type = 'time'


class VegetableForm(ModelForm):
    """ Model form based on the Vegetable model """
    class Meta:
        model = Variety
        fields = ['french_name', 'latin_name']


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
        widgets = {
            'duration': CustomTimeInput(attrs={'step': 1}),
        }
