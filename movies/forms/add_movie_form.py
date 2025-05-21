from django import forms
from movies.models.movie import Movie

class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        widgets = {
            'release_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
