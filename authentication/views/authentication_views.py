import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

logger = logging.getLogger('django')

def login_page(request):
    """
    Handles user login functionality.

    - If the user is already authenticated, redirects to the 'no_permission' page.
    - On POST request:
        - Retrieves the username and password from the form.
        - Validates the existence of the user.
        - Authenticates the credentials.
        - If authentication fails, displays appropriate error messages.
        - If authentication succeeds, logs the user in and redirects to the movie list page.
    - On GET request, renders the login page.

    In case of unexpected errors, logs the exception and redirects to a generic error page.
    """
    try:
        if request.user.is_authenticated:
            return redirect('no_permission')
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Check if a user with the provided username exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid Username')
                return redirect('/login/')

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is None:
                # Display an error message if authentication fails (invalid password)
                messages.error(request, "Invalid Password")
                return redirect('/login/')
            else:
                # Log in the user and redirect to the home page upon successful login
                login(request, user)
                return redirect('movie_list')

        return render(request, 'login.html')

    except Exception as e:
        logger.error(f'Error while logging in. {str(e)}', exc_info=True)
        return redirect('error_page')


def register_page(request):
    """
        Handles user registration functionality.

        - If the user is already authenticated, redirects to the 'no_permission' page.
        - On POST request:
            - Retrieves form data for first name, last name, username, and password.
            - Checks if a user with the provided username already exists.
                - If yes, displays an info message and reloads the registration page.
            - Creates a new user with the provided credentials.
            - Sets the password and saves the user.
            - Attempts to assign the user to the 'Client' group.
                - If the group doesn't exist, displays an error message.
            - Displays a success message and reloads the registration page.
        - On GET request, renders the registration page.

        Logs any unexpected exceptions and redirects to a generic error page.
    """
    try:
        if request.user.is_authenticated:
            return redirect('no_permission')
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Check if a user with the provided username already exists
            user = User.objects.filter(username=username)

            if user.exists():
                messages.info(request, "Username already taken!")
                return redirect('/register/')

            # Create a new User
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username
            )

            user.set_password(password)
            user.save()

            try:
                group = Group.objects.get(name='Client')
                user.groups.add(group)
            except Group.DoesNotExist:
                messages.error(request, "Client role does not exist!")
                return redirect('/register/')

            messages.info(request, "Account created Successfully!")
            return redirect('/register/')

        return render(request, 'register.html')

    except Exception as e:
        logger.error(f'Error while registering. {str(e)}', exc_info=True)
        return redirect('error_page')


@login_required
def logout_view(request):
    """
    Logs out the currently authenticated user and redirects to the login page.
    """
    logout(request)
    return redirect('login_page')

def no_permission(request):
    """
     Renders a page informing the user that they do not have permission to access the requested resource.
    """
    return render(request, 'no_permission.html')

def error_page(request):
    """
    Renders a generic error page to inform the user that an unexpected error has occurred.
    """
    return  render(request, 'error.html')

def default_redirect(request):
    """
    Redirect the user to the movie list page.
    """
    return redirect('movie_list')