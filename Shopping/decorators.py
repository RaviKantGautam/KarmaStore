from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_client and request.user.is_active:
            return redirect('/Shopping')
        return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_client and request.user.is_active and request.user.is_authenticated:
                return wrapper_func
            else:
                return HttpResponse('You are not authorize to view this page')
            # group = None
            # if request.user.groups.exists():
            #     group = request.user.groups.all()[0].name
            # if group in allowed_roles:
            #     return view_func(request,*args,**kwargs)
            # else:
            #     return HttpResponse('You are not authorized to view this page')

    return decorator
