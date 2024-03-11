from django.shortcuts import render
from .models import Hackathon

def landing_page(request):
    hackathon = Hackathon.objects.first()  # Assuming there's only one hackathon
    return render(request, 'landing_page.html', {'hackathon': hackathon})

def login_page(request):
    # Add your login logic here
    return render(request, 'login.html')

def sign_up_page(request):
    # Add your sign-up logic here
    return render(request, 'sign_up.html')
