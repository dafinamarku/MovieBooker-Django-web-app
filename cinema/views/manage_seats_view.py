from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from cinema.models import Room, Seat
import logging

logger = logging.getLogger('django')

@login_required
def manage_seats(request, room_id):
    """
    View for managing seats in a specific room, accessible only to Admin users.

    Allows Admin users to:
        - Add a new row of seats (adds a seat with number 1 in the next alphabetical row).
        - Add a seat to an existing row (adds a seat with the next seat number in that row).
        - Remove the last seat from a specified row.

    Seats are grouped by rows and passed to the template for display.

    Args:
        request (HttpRequest): The HTTP request object.
        room_id (int): The ID of the Room to manage seats for.

    Returns:
        HttpResponse: Rendered 'manage_seats.html' template with seat data if GET request,
                      or redirects back to the same page after POST actions.
                      Redirects to 'no_permission' if user is not Admin,
                      or to 'error_page' if an unexpected error occurs.
    """
    try:
        if not request.user.groups.filter(name='Admin').exists():
            return redirect('no_permission')

        room = get_object_or_404(Room, pk=room_id)
        seats = Seat.objects.filter(room=room).order_by('row', 'number')

        if request.method == 'POST':
            if 'add_row' in request.POST:
                last_row = seats.order_by('-row').first()
                next_row_letter = chr(ord(last_row.row) + 1) if last_row else 'A'
                new_seat = Seat.objects.create(room=room, row=next_row_letter, number=1)
                new_seat.created_by = request.user
                new_seat.changed_by = request.user
                new_seat.save()

                messages.success(request, f"Added row {next_row_letter}")
                return redirect(request.path_info)

            for key in request.POST:
                if key.startswith('add_seat_'):
                    row_letter = key.split('_')[-1]
                    last_seat = seats.filter(row=row_letter).order_by('-number').first()
                    next_number = last_seat.number + 1 if last_seat else 1
                    new_seat = Seat.objects.create(room=room, row=row_letter, number=next_number)
                    new_seat.created_by = request.user
                    new_seat.changed_by = request.user
                    new_seat.save()

                    messages.success(request, f"Added seat {row_letter}{next_number}")
                    return redirect(request.path_info)

                if key.startswith('remove_seat_'):
                    row_letter = key.split('_')[-1]
                    last_seat = seats.filter(row=row_letter).order_by('-number').first()
                    if last_seat:
                        last_seat.delete()
                        messages.success(request, f"Removed seat {row_letter}{last_seat.number}")
                    return redirect(request.path_info)

        # group seats
        rows = {}
        for seat in seats:
            rows.setdefault(seat.row, []).append(seat.number)

        return render(request, 'manage_seats.html', {
            'room': room,
            'rows': rows,
        })

    except Exception as e:
        logger.error(f'Error managing seats for room {room_id}: {str(e)}', exc_info=True)
        return redirect('error_page')
