
def is_user_admin(request):
    """
    Context processor that returns whether the current user belongs to the 'Admin' group.

    Args:
        request (HttpRequest): The current request object.

    Returns:
        dict: A dictionary with key 'is_user_admin' and a boolean value indicating
              if the authenticated user is in the 'Admin' group. Returns False if the user is anonymous.
    """
    return {
        'is_user_admin': request.user.groups.filter(name='Admin').exists() if request.user.is_authenticated else False
    }

def is_user_client(request):
    """
        Context processor that returns whether the current user belongs to the 'Client' group.

        Args:
            request (HttpRequest): The current request object.

        Returns:
            dict: A dictionary with key 'is_user_client' and a boolean value indicating
                  if the authenticated user is in the 'Client' group. Returns False if the user is anonymous.
    """
    return {
        'is_user_client': request.user.groups.filter(name='Client').exists() if request.user.is_authenticated else False
    }
