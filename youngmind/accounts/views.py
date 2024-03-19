from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from .models import Account,Team, TeamMember
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from .forms import CollegeFacultySignUpForm, StudentSignUpForm,TeamMemberRegistrationForm


User = get_user_model()

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        team_member_form = TeamMemberRegistrationForm(request.POST, request.FILES)
        if form.is_valid() and team_member_form.is_valid():
            # Save the StudentSignUpForm data
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the user until email verification is complete
            user.save()

            # Save the TeamMemberRegistrationForm data
            team_member = team_member_form.save(commit=False)
            team_member.save()

            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return redirect('account_activation_sent')
    else:
        form = StudentSignUpForm()
        team_member_form = TeamMemberRegistrationForm()

    return render(request, 'student_signup.html', {'form': form, 'team_member_form': team_member_form})

def faculty_signup(request):
    if request.method == 'POST':
        form = CollegeFacultySignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return redirect('account_activation_sent')
    else:
        form = CollegeFacultySignUpForm()

    return render(request, 'faculty_signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')




from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type', None)

        # Manually log in the user
        user = get_user_model().objects.get(email=email)
        auth_login(request, user)

        messages.success(request, 'You are now logged in.')
        if user_type == 'CollegeFaculty':
            return redirect('dashboard')
        elif user_type == 'CollegeStudent':
            return render(request, 'team_member_register.html')
    
    return render(request, 'accounts/login.html', {'messages': messages.get_messages(request)})

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})