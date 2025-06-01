import logging
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cinema.models import Screening, Seat, Ticket

logger = logging.getLogger('django')

@login_required
def ticket_book_view(request, screening_id):
    """
        Handles the ticket booking process for a given screening.

        This view:
            - Retrieves the screening and associated room.
            - Displays all seats in the room, marking those that are already taken.
            - If the request method is POST, processes the selected seats:
                - Creates tickets for available seats.
                - Adds messages for seats that were already booked or successfully booked.
            - Redirects back to the movie display page after processing.
            - Renders the ticket booking template on GET requests.

        In case of an unexpected error, logs the exception and redirects to a generic error page.

        Args:
            request (HttpRequest): The HTTP request object.
            screening_id (int): The ID of the screening for which the ticket is being booked.

        Returns:
            HttpResponse: The rendered booking page or a redirect based on the outcome.
    """
    try:
        screening = get_object_or_404(Screening, pk=screening_id)
        room = screening.room
        all_seats = Seat.objects.filter(room=room)
        taken_seats = Ticket.objects.filter(screening=screening).values_list('seat_id', flat=True)

        rows = {}
        for seat in all_seats:
            rows.setdefault(seat.row, []).append({
                'id': seat.id,
                'number': seat.number,
                'is_taken': seat.id in taken_seats
            })

        if request.method == 'POST':
            selected_seats = request.POST.getlist('seats')
            already_booked_seats = list()
            successfully_booked_seats = list()

            if selected_seats:
                for seat_id in selected_seats:
                    seat = get_object_or_404(Seat, pk=seat_id, room=room)

                    # check if seat is still available
                    if not Ticket.objects.filter(screening=screening, seat=seat).exists():
                        Ticket.objects.create(screening=screening, seat=seat, user=request.user)
                        successfully_booked_seats.append(seat)
                    else:
                        already_booked_seats.append(seat)

                already_booked_seats_count = len(already_booked_seats)
                if already_booked_seats_count > 0:
                    already_booked_seats_str = ", ".join(str(seat) for seat in already_booked_seats)
                    if already_booked_seats_count == 1:
                        msg = 'Seat: ' + already_booked_seats_str + ' is already booked.'
                    else:
                        msg = 'Seats: ' + already_booked_seats_str + ' are already booked.'
                    messages.error(request, msg)

                successfully_booked_seats_count = len(successfully_booked_seats)
                if successfully_booked_seats_count > 0:
                    successfully_booked_seats_str = ", ".join(str(seat) for seat in successfully_booked_seats)
                    if successfully_booked_seats_count == 1:
                        success_msg = 'Seat: ' + successfully_booked_seats_str + ' is successfully booked.'
                    else:
                        success_msg = 'Seats: ' + successfully_booked_seats_str + ' are successfully booked.'
                    messages.success(request, success_msg)

                return redirect('movie_display', movie_id=screening.movie.id)

        return render(request, 'ticket_book.html', {
            'screening': screening,
            'rows': rows,
        })

    except Exception as e:
        logger.error(f'Error while booking ticket. {str(e)}', exc_info=True)
        return redirect('error_page')

