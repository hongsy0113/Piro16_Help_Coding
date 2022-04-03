from django.template import RequestContext
from django.shortcuts import render, redirect


# 404 Error
def page_not_found(request, exception):
    return render(request, 'error.html', status=404)

# 500 Error
def server_error(request, exception):
    return render(request, 'error.html', status=500)

# 400 Error
def bad_request(request, exception):
    return render(request, 'error.html', status=400)
