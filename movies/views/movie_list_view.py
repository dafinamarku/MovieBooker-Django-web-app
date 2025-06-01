import logging
from django.shortcuts import render, redirect
from movies.models import Movie

logger = logging.getLogger('django')

def movie_list(request):
    """
        Displays a list of all movies, optionally filtered by a search query.

        This view:
            - Retrieves the optional 'search' parameter from the GET request.
            - If a query is provided, filters movies whose title contains the query string (case-insensitive).
            - Otherwise, returns all available movies.
            - Renders the 'movie_list.html' template with the list of movies and the query (if any).

        In case of an exception, logs the error and redirects to a generic error page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered movie list page or a redirect to the error page.
        """
    try:
        query = request.GET.get('search')
        if query:
            movies = Movie.objects.filter(title__icontains=query)
        else:
            movies = Movie.objects.all()

        return render(request, 'movie_list.html', {
            'movies': movies,
            'query': query
        })
    except Exception as e:
        logger.error(f'Error while registering. {str(e)}', exc_info=True)
        return redirect('error_page')
