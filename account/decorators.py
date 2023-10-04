from django.shortcuts import redirect
from django.urls import reverse
#decorators to check whether user is already logged in or not.
def authentication_not_required(view_func,):
    def wrapper(request, *args,**kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        #if user is already logged in, redirect to the respective dashboard
        redirect_url = reverse(f'main:dashboard')
        
        return redirect(redirect_url)
    
    return wrapper

#decorators to verify whether user types is admin or not

#decorator to verify whether user type is superadmin or not
