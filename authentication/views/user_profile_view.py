import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cinema.models import Ticket

logger = logging.getLogger('django')

@login_required
def user_profile(request):
    """
        Render the user profile page showing tickets grouped by screening.

        Retrieves all tickets booked by the currently authenticated user,
        including related screening, movie, room, and seat data. Tickets are
        ordered by the screening's start time in descending order and grouped
        by screening for display.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: Rendered 'user_profile.html' template with grouped tickets
            and user data if successful, otherwise redirects to 'error_page' on failure.
    """
    try:
        tickets = (
            Ticket.objects.filter(user=request.user)
            .select_related('screening__movie', 'screening__room', 'seat')
            .order_by('-screening__start_time')
        )

        # group by screening
        from collections import defaultdict
        grouped_tickets = defaultdict(list)
        for ticket in tickets:
            grouped_tickets[ticket.screening].append(ticket)

        return render(request, 'user_profile.html', {
            'grouped_tickets': dict(grouped_tickets),
            'user': request.user
        })

    except Exception as e:
        logger.error(f'Error while loading user profile. {str(e)}', exc_info=True)
        return redirect('error_page')

