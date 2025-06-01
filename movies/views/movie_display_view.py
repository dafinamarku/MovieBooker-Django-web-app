import logging
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from cinema.models import Screening
from movies.models.movie import Movie

logger = logging.getLogger('django')

def movie_display(request, movie_id):
    """
    Displays details of a specific movie along with its associated screenings.

    This view:
        - Retrieves the Movie object by its ID.
        - Fetches all related Screening objects ordered by start time in descending order.
        - Renders the 'movie_display.html' template with movie and screening data.

    In case of an exception (e.g., movie not found), logs the error and redirects to a generic error page.

    Args:
        request (HttpRequest): The HTTP request object.
        movie_id (int): The ID of the movie to be displayed.

    Returns:
        HttpResponse: The rendered movie detail page or a redirect to the error page.
    """
    try:
        movie = get_object_or_404(Movie, id=movie_id)
        screenings = Screening.objects.filter(movie=movie).order_by('-start_time')

        return render(request, 'movie_display.html', {
            'movie': movie,
            'screenings': screenings
        })

    except Exception as e:
        logger.error(f'Error displaying movie. {str(e)}', exc_info=True)
        return redirect('error_page')

