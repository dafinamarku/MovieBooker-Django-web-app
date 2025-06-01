import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cinema.models import Room

logger = logging.getLogger('django')

@login_required
def room_list(request):
    """
    Displays a list of all rooms. Only accessible by admin users.

    This view:
        - Verifies that the current user belongs to the 'Admin' group.
        - Retrieves all Room instances from the database.
        - Renders the 'room_list.html' template with the list of rooms.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Renders the list of rooms,
                      or redirects to 'no_permission' if the user is not an admin,
                      or to 'error_page' if an exception occurs.
    """
    try:
        if not request.user.groups.filter(name='Admin').exists():
            return redirect('no_permission')

        rooms = Room.objects.all()

        return render(request, 'room_list.html', {
            'rooms': rooms
        })
    except Exception as e:
        logger.error(f'Error displaying room list. {str(e)}', exc_info=True)
        return redirect('error_page')

