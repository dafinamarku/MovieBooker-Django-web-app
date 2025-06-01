from django import forms
from django.forms import inlineformset_factory
from cinema.models import Room, Seat


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'name',
            'opening_time',
            'closing_time'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'opening_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'closing_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
        }
