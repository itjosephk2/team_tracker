import secrets
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.mail import send_mail
from people_management.models import Person

class CustomUserCreationForm(UserCreationForm):
    """
    Admin-only form to create a new user linked to a Person.
    - Auto-generates a secure password.
    - Emails the user their login details.
    - Pulls first name, last name, and email from the Person model.
    - Optionally assigns a group.
    """
    person = forms.ModelChoiceField(
        queryset=Person.objects.filter(user__isnull=True),  # Only show unlinked persons
        required=True,
        label="Select Employee",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Assign Group",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "person", "group"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}),
        }
        help_texts = {"username": ""}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_person(self):
        person = self.cleaned_data.get("person")
        if person and person.user:
            raise forms.ValidationError("This person is already linked to another user.")
        return person

    def save(self, commit=True):
        user = super().save(commit=False)
        person = self.cleaned_data.get("person")

        # Pull details from the Person model
        user.first_name = person.first_name
        user.last_name = person.last_name
        user.email = person.email

        # Generate a secure random password
        random_password = secrets.token_urlsafe(12)
        user.set_password(random_password)

        if commit:
            user.save()
            # Link the Person to the User
            person.user = user
            person.save()

            # Assign group if one was selected
            group = self.cleaned_data.get("group")
            if group:
                user.groups.add(group)

            # Send email with login credentials
            send_mail(
                "Your New Account Credentials",
                f"Hello {user.first_name},\n\n"
                f"Your account has been created.\n"
                f"Username: {user.username}\n"
                f"Password: {random_password}\n\n"
                "Please log in and change your password.",
                "admin@yourdomain.com",  # Replace with your actual sender email
                [user.email],
                fail_silently=True,
            )

        return user


class CustomLoginForm(AuthenticationForm):
    """
    Custom login form.
    Currently, it simply extends Django's built-in AuthenticationForm,
    but can be customized further if needed.
    """
    pass


class UserForm(forms.ModelForm):
    """
    A form for updating a user's details and linking them to a Person.
    This can be used for editing existing users.
    """
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=True,
        label="Link Employee",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "person"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
