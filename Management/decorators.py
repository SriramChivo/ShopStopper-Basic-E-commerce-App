from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def AllowedUsers(allowedroles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            grp = request.user.groups.all()
            for i in grp:
                if(i.name in allowedroles):
                    return view_func(request, *args, **kwargs)
                else:
                    print("not working")
                    return HttpResponseRedirect(reverse("Unauth"))
        return(wrapper_func)
    return(decorator)
