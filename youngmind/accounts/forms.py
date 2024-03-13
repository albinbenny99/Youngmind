from django import forms
from .models import Account

class CollegeFacultySignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    user_role = forms.CharField(widget=forms.HiddenInput(), initial='CollegeFaculty')

    class Meta:
        model = Account
        fields = ['email', 'password', 'confirm_password', 'user_role', 'aishe_code','college_name', 'state', 'city', 'district', 'college_address', 'college_pincode', 'faculty_first_name', 'faculty_last_name', 'faculty_designation', 'faculty_mobile_number', 'spoc_consent_letter', 'college_logo']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

class StudentSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    user_role = forms.CharField(widget=forms.HiddenInput(), initial='Student')

    class Meta:
        model = Account
        fields = ['email', 'password', 'confirm_password', 'user_role', 'team_leader_first_name', 'team_leader_last_name','college_name', 'state', 'city', 'district', 'faculty_name', 'faculty_designation', 'mobile_number', 'faculty_email_id', 'photo', 'verification_document']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password
