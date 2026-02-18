from functools import wraps
from django.shortcuts import redirect

def student_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get("student_auid"):
            return redirect("student_login")
        return view_func(request, *args, **kwargs)
    return _wrapped
