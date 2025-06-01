from django import forms
from movies.models.movie import Movie

class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title',
            'genres',
            'description',
            'photo',
            'release_date',
            'duration_in_minutes',
            'age_limit',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'genres': forms.SelectMultiple(attrs={
                'class': 'form-select multiselect-dropdown'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'release_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'duration_in_minutes': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'age_limit': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Movie Title',
            'genres': 'Genres',
            'description': 'Description',
            'photo': 'Poster/Image',
            'release_date': 'Release Date',
            'duration_in_minutes': 'Duration (minutes)',
            'age_limit': 'Age Limit',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Movie.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This movie title already exists.")
        return title

    def clean(self):
        cleaned_data = super().clean()
        release_date = cleaned_data.get('release_date')
        duration = cleaned_data.get('duration_in_minutes')
        age_limit = cleaned_data.get('age_limit')

        if duration is not None and duration <= 0:
            self.add_error('duration_in_minutes', 'Duration must be a positive number.')

        if age_limit is not None and (age_limit < 0 or age_limit > 21):
            self.add_error('age_limit', 'Age limit must be between 0 and 21.')

        return cleaned_data
