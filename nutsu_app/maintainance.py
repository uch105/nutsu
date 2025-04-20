from django.shortcuts import render

def home(request):
    return render(request, "nutsu_app/maintainance.html")