from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from movies.forms.add_movie_form import AddMovieForm
from django.contrib import messages
import logging
from movies.models import Movie

logger = logging.getLogger('django')

@login_required
def create_or_edit_movie(request, pk=None):
    """
    Handles both the creation and editing of a Movie object.

    This view:
        - Restricts access to users in the 'Admin' group.
        - If `pk` is provided, it fetches the corresponding Movie for editing; otherwise, prepares for creation.
        - On POST request:
            - Validates and saves the movie form.
            - Sets created_by and changed_by fields appropriately.
            - Displays success message and redirects to the movie list.
        - On GET request:
            - Displays the form with existing data if editing, or an empty form if creating.

    In case of any exception, logs the error and redirects to a generic error page.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int, optional): The primary key of the movie to edit. If None, creates a new movie.

    Returns:
        HttpResponse: The rendered add/edit movie page or a redirect.
    """
    try:
        if not request.user.groups.filter(name='Admin').exists():
            return redirect('no_permission')

        if pk:
            movie = get_object_or_404(Movie, pk=pk)
            is_edit = True
        else:
            movie = None
            is_edit = False

        if request.method == 'POST':
            form = AddMovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                movie = form.save(commit=False)
                if not is_edit:
                    movie.created_by = request.user
                movie.changed_by = request.user
                movie.save()
                form.save_m2m()

                msg = 'Movie updated successfully.' if is_edit else 'Movie created successfully.'
                messages.success(request, msg)
                return redirect('movie_list')
        else:
            form = AddMovieForm(instance=movie)

    except Exception as e:
        logger.error(f'Error creating/editing movie: {str(e)}', exc_info=True)
        return redirect('error_page')

    return render(request, 'add_movie.html', {
        'form': form,
        'is_edit': is_edit,
    })

