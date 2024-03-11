from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_page, name='login_page'),
    path('sign-up/', views.sign_up_page, name='sign_up_page'),
    
]
