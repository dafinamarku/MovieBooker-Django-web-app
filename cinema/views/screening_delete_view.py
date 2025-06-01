import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from cinema.models import Screening

logger = logging.getLogger('django')

@require_POST
@login_required
def screening_delete(request, screening_id):
    """
        Deletes a screening if it has no associated tickets.

        This view:
            - Requires the user to be logged in and sends a POST request.
            - Fetches the screening based on the given screening_id.
            - If the screening has any tickets associated with it, deletion is blocked and an error message is shown.
            - Otherwise, deletes the screening and shows a success message.
            - Redirects back to the movie display page.

        In case of an unexpected error, redirects to a generic error page.

        Args:
            request (HttpRequest): The HTTP request object.
            screening_id (int): The ID of the screening to be deleted.

        Returns:
            HttpResponseRedirect: A redirect to the appropriate page based on outcome.
    """
    try:
        screening = get_object_or_404(Screening, pk=screening_id)

        if screening.ticket_set.exists():
            messages.error(request, "This screening has tickets and cannot be deleted.")
            return redirect('movie_display', movie_id=screening.movie.id)

        screening.delete()
        messages.success(request, "Screening deleted successfully.")
        return redirect('movie_display', movie_id=screening.movie.id)

    except Exception as e:
        logger.error(f'Error while deleting screening. {str(e)}', exc_info=True)
        return redirect('error_page')
