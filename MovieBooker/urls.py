"""
URL configuration for MovieBooker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path       # URL routing
from authentication.views import *
from django.conf import settings   # Application settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Static files serving

from authentication.views.authentication_views import no_permission
from cinema.views import *
from movies.views import *

# Define URL patterns
urlpatterns = [
    path('', default_redirect, name='default'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('register/', register_page, name='register'),
    path('movies/add/', create_or_edit_movie, name='create_movie'),
    path('movies/edit/<int:pk>/', create_or_edit_movie, name='edit_movie'),
    path('movies/all', movie_list, name='movie_list'),
    path('movies/display/<int:movie_id>/', movie_display, name='movie_display'),
    path('rooms/add/', room_create_or_update, name='room_add'),
    path('rooms/edit/<int:pk>/', room_create_or_update, name='room_edit'),
    path('rooms/display/<int:room_id>/', room_display, name='room_display'),
    path('rooms/seats/<int:room_id>/', manage_seats, name='manage_seats'),
    path('rooms/all/', room_list, name='room_list'),
    path('screenings/add/<int:movie_id>/', screening_add, name='screening_add'),
    path('screenings/available-rooms/', get_available_rooms, name='available_rooms'),
    path('screenings/delete/<int:screening_id>/', screening_delete, name='screening_delete'),
    path('ticket/book/<int:screening_id>/', ticket_book_view, name='ticket_book'),
    path('no-permission/', no_permission, name='no_permission'),
    path('error/', error_page, name='error_page'),
]

# Serve media files if DEBUG is True (development mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files using staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
