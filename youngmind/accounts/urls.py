from django.urls import path
from . import views

urlpatterns = [
     path('student/signup/', views.student_signup, name='student_signup'),
    path('faculty/signup/', views.faculty_signup, name='faculty_signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forgotPassword, name='forgotPassword'),
    path('reset-password/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('reset-password/', views.resetPassword, name='resetPassword'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
]
