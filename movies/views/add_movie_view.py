from django.shortcuts import render, redirect
from movies.forms.add_movie_form import AddMovieForm


def create_movie(request):
    if request.method == 'POST':
        form = AddMovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = AddMovieForm()
    return render(request, 'add_movie.html', {'form': form})
