import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cinema.forms import RoomForm
from cinema.models import Room

logger = logging.getLogger('django')

@login_required
def room_create_or_update(request, pk=None):
    """
    Create a new room or update an existing one, accessible only to Admin users.

    - If `pk` is provided, the view fetches the existing Room instance for editing.
    - If no `pk` is provided, the view creates a new Room.
    - Only users in the 'Admin' group are allowed to access this view.
    - On POST, the submitted RoomForm is validated and saved.
    - Sets `created_by` only on new rooms and always updates `changed_by`.
    - On successful save, redirects to the 'room_list' page.
    - On GET, renders the form with current room data if editing, or empty form if creating.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int, optional): Primary key of the Room to edit. Defaults to None for creating a new Room.

    Returns:
        HttpResponse: Renders the 'room_create_or_update.html' template with the form,
                      or redirects to 'room_list' on success,
                      'no_permission' if user lacks admin rights,
                      or 'error_page' if an unexpected error occurs.
    """
    try:
        if not request.user.groups.filter(name='Admin').exists():
            return redirect('no_permission')

        if pk:
            room = get_object_or_404(Room, pk=pk)
            is_edit = True
        else:
            room = None
            is_edit = False

        if request.method == 'POST':
            form = RoomForm(request.POST, instance=room)

            if form.is_valid():
                room = form.save(commit=False)
                if not is_edit:
                    room.created_by = request.user
                room.changed_by = request.user
                room.save()

                messages.success(request, 'Room saved successfully.')
                return redirect('room_list')

        else:
            form = RoomForm(instance=room)

        return render(request, 'room_create_or_update.html', {
            'form': form,
            'is_edit': is_edit,
        })

    except Exception as e:
        logger.error(f'Error creating/editing room: {str(e)}', exc_info=True)
        return redirect('error_page')
