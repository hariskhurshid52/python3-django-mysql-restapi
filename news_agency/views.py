from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def dashboard(request):
    view_data = {
        "title": "haris"
    }
    return render(request, 'dashboard.html', view_data);
