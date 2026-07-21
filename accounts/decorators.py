from django.shortcuts import redirect
from functools import wraps


def employer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if (
            request.user.is_authenticated and
            request.user.profile.role == "employer"
        ):
            return view_func(request, *args, **kwargs)

        return redirect("home")

    return wrapper


def seeker_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if (

            request.user.is_authenticated and

            request.user.profile.role == "seeker"

        ):
            return view_func(request, *args, **kwargs)

        return redirect("home")

    return wrapper