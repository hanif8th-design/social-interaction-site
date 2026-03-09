from django.shortcuts import redirect
from functools import wraps


def redirect_if_logged_in(view_func):
    #redirect logged in user to home page
    @wraps(view_func)  #wrapper replaces our origional login view temporarily
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:home")
        return view_func(request, *args, **kwargs)
    return wrapper
