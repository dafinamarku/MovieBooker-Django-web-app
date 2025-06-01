import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from cinema.models import Room, Seat

logger = logging.getLogger('django')

@login_required
def room_display(request, room_id):
    """
    Displays the seating arrangement of a specific room. Only accessible by admin users.

    This view:
        - Checks if the current user belongs to the 'Admin' group.
        - Retrieves the specified Room and its associated seats ordered by row and number.
        - Groups seats by row to make them easier to render in the template.
        - Renders the 'room_display.html' template with the room and grouped seat data.

    Args:
        request (HttpRequest): The incoming HTTP request.
        room_id (int): The primary key of the room to be displayed.

    Returns:
        HttpResponse: Renders the seating layout page for the room,
                      or redirects to 'no_permission' if the user is not an admin,
                      or to 'error_page' if an exception occurs.
    """
    try:
        if not request.user.groups.filter(name='Admin').exists():
            return redirect('no_permission')

        room = get_object_or_404(Room, id=room_id)
        seats = Seat.objects.filter(room=room).order_by('row', 'number')

        # group seats
        rows = {}
        for seat in seats:
            rows.setdefault(seat.row, []).append(seat.number)

        return render(request, 'room_display.html', {'room': room, 'rows': rows})

    except Exception as e:
        logger.error(f'Error displaying room {room_id}: {str(e)}', exc_info=True)
        return redirect('error_page')