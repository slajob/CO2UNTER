from django import forms
from .models import CO2Consumption

class CO2ConsumptionForm(forms.ModelForm):
    class Meta:
        model = CO2Consumption
        exclude = ['user']
        widgets = {
            'waste_segregation': forms.RadioSelect(choices=((True, 'Tak'), (False, 'Nie'))),
            'air_conditioning': forms.RadioSelect(choices=((True, 'Tak'), (False, 'Nie'))),
            'heating_method': forms.RadioSelect(),
            'everyday_travel': forms.RadioSelect(),
            'diet': forms.RadioSelect(),
            'clothes_shopping_frequency': forms.RadioSelect(),
            'air_travel_frequency': forms.NumberInput(),
            'going_out_frequency': forms.RadioSelect(),
            'disposable_packaging': forms.RadioSelect(choices=((True, 'Tak'), (False, 'Nie'))),
            'mass_event_frequency': forms.RadioSelect(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field].widget, forms.NumberInput):
                self.fields[field].widget.attrs['class'] = 'input'
            elif isinstance(self.fields[field].widget, forms.RadioSelect):
                self.fields[field].widget.attrs['class'] = 'radio'