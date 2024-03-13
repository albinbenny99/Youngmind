from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, user_role='Student', **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            user_role=user_role,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_role', 'Admin')
        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser):
    USER_ROLE_CHOICES = (
        ('CollegeFaculty', 'College Faculty SPOC'),
        ('Student', 'Student')
    )

    # Common fields for both roles
    email = models.EmailField(max_length=100, unique=True)
    user_role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES, default='Student')
    password = models.CharField(max_length=255)

    # Fields for College Faculty
    aishe_code = models.CharField(max_length=50, blank=True, null=True)

    college_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    college_address = models.TextField(blank=True, null=True)
    college_pincode = models.CharField(max_length=10, blank=True, null=True)
    faculty_first_name = models.CharField(max_length=50, blank=True, null=True)
    faculty_last_name = models.CharField(max_length=50, blank=True, null=True)
    faculty_designation = models.CharField(max_length=255, blank=True, null=True)
    create_password = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    spoc_consent_letter = models.FileField(upload_to='spoc_consent_letters/', blank=True, null=True)
    college_logo = models.ImageField(upload_to='college_logos/', blank=True, null=True)

    # Fields for College Student
    team_leader_first_name = models.CharField(max_length=50, blank=True, null=True)
    team_leader_last_name = models.CharField(max_length=50, blank=True, null=True)
    new_password = models.CharField(max_length=255, blank=True, null=True)
    
    faculty_name = models.CharField(max_length=255, blank=True, null=True)
    faculty_designation = models.CharField(max_length=255, blank=True, null=True)
    faculty_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    faculty_email_id = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    verification_document = models.FileField(upload_to='verification_documents/', blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
