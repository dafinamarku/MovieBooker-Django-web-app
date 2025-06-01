import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from datetime import timedelta
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_GET
from cinema.forms.screening_form import ScreeningForm
from cinema.models import Screening, Room
from movies.models import Movie

logger = logging.getLogger('django')

@login_required
def screening_add(request, movie_id):
    """
    Allows admin users to add a new screening for a given movie.

    This view:
    - Ensures the user is in the 'Admin' group.
    - Retrieves the specified movie using its ID.
    - Handles POST requests to create a new Screening using the submitted form data.
    - Automatically sets the `created_by` and `changed_by` fields.
    - On success, redirects to the movie display page.
    - On GET requests, initializes the form with the selected movie.

    Args:
        request (HttpRequest): The incoming HTTP request.
        movie_id (int): The ID of the movie to add a screening for.

    Returns:
        HttpResponse: Renders the 'screening_add.html' template,
                      or redirects to 'no_permission' if the user is not an admin,
                      or to 'error_page' if an exception occurs.
    """
    try:
        if not request.user.groups.filter(name='Admin').exists():
            return redirect('no_permission')

        movie = get_object_or_404(Movie, pk=movie_id)

        if request.method == 'POST':
            form = ScreeningForm(request.POST)
            if form.is_valid():
                screening = form.save(commit=False)
                screening.created_by = request.user
                screening.changed_by = request.user
                screening.save()

                messages.success(request, 'Screening saved successfully.')

                return redirect('movie_display', movie_id=movie.id)
        else:
            form = ScreeningForm(initial={'movie': movie})

        return render(request, 'screening_add.html', {
            'form': form,
            'movie': movie
        })

    except Exception as e:
        logger.error(f'Error while adding screening. {str(e)}', exc_info=True)
        return redirect('error_page')

@login_required
@require_GET
def get_available_rooms(request):
    """
        Returns a list of available rooms for a given movie and start time.

        This view:
            - Expects `start_time` and `movie_id` as GET parameters.
            - Parses the start time and calculates the end time based on the movie's duration.
            - Finds rooms that are already booked during the selected time.
            - Excludes busy rooms and filters out rooms that are closed during the screening period.
            - Returns the list of available rooms as a JSON response.

        Returns:
            JsonResponse: A dictionary containing either:
                - {'rooms': [{'id': ..., 'name': ...}, ...]} if successful.
                - {'error': '...'} with status 400 if an error occurs.
    """
    start_time_str = request.GET.get('start_time')
    movie_id = request.GET.get('movie_id')

    try:
        start_time = parse_datetime(start_time_str)
        movie = Movie.objects.get(id=movie_id)
        end_time = start_time + timedelta(minutes=movie.duration_in_minutes)

        busy_rooms = Screening.objects.filter(
            start_time__lt=end_time,
            movie__isnull=False
        ).annotate(
            existing_end=models.ExpressionWrapper(
                models.F('start_time') + models.functions.Cast(
                    models.F('movie__duration_in_minutes') * 60,
                    models.DurationField()
                ),
                output_field=models.DateTimeField()
            )
        ).filter(
            existing_end__gt=start_time
        ).values_list('room_id', flat=True)

        available_rooms = Room.objects.exclude(id__in=busy_rooms).filter(
            opening_time__lte=start_time.time(),
            closing_time__gte=end_time.time()
        )

        room_list = [{'id': room.id, 'name': room.name} for room in available_rooms]
        return JsonResponse({'rooms': room_list})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
