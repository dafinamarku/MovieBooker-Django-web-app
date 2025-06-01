from django import forms
from django.forms.widgets import DateTimeInput
from cinema.models import Screening


class ScreeningForm(forms.ModelForm):
    end_time = forms.DateTimeField(
        required=False,
        widget=DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'disabled': 'disabled'
        }),
        label="End time"
    )
    class Meta:
        model = Screening
        fields = [
            'start_time',
            'room',
            'movie'
        ]
        widgets = {
            'movie': forms.HiddenInput(),
            'start_time': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }