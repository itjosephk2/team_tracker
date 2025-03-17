import secrets
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.mail import send_mail
from people_management.models import Person


class CustomUserCreationForm(UserCreationForm):
    """
    Form for admin to create a new user linked to a Person.
    - Only allows selecting employees (Persons) who are not already linked to a user.
    - Optionally assigns the user to a group.
    - Generates a secure password and emails the user.
    """
    password1 = forms.CharField(widget=forms.HiddenInput(), required=False, label='')
    password2 = forms.CharField(widget=forms.HiddenInput(), required=False, label='')
    person = forms.ModelChoiceField(
        queryset=Person.objects.filter(user__isnull=True),  # Only show unlinked persons
        required=True,
        label="Select Employee",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Assign Permissions Group",
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
        """Ensure the username is unique."""
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_person(self):
        """Ensure the selected person is not already linked to a user."""
        person = self.cleaned_data.get("person")
        if person and person.user:
            raise forms.ValidationError("This person is already linked to another user.")
        return person

    def save(self, commit=True):
        """
        Create a new user and link it to the selected Person.
        Generates a secure password and sends login credentials via email.
        """
        user = super().save(commit=False)
        person = self.cleaned_data.get("person")
        user.first_name = person.first_name
        user.last_name = person.last_name
        user.email = person.email

        random_password = secrets.token_urlsafe(12)
        user.set_password(random_password)

        if commit:
            user.save()
            person.user = user
            person.save()

            group = self.cleaned_data.get("group")
            if group:
                user.groups.add(group)

            send_mail(
                "Your New Account Credentials",
                f"Hello {user.first_name},\n\nYour account has been created.\nUsername: {user.username}\nPassword: {random_password}\n\nPlease log in and change your password.",
                "admin@yourdomain.com",
                [user.email],
                fail_silently=False,
            )
            print(f"Generated Password for {user.username}: {random_password}")
        return user


class CustomLoginForm(AuthenticationForm):
    """Custom login form extending Django's default authentication form."""
    pass


class PersonForm(forms.ModelForm):
    """
    Form for linking a Person to a User.
    Only displays Users who are not already linked to a Person.
    """
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(person__isnull=True),  # Exclude already linked users
        required=False
    )

    class Meta:
        model = Person
        fields = ["user"]


class UserForm(forms.ModelForm):
    """Form for updating basic User details (excluding email)."""
    class Meta:
        model = User
        fields = ["username", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.Select(attrs={"class": "form-select"}),
        }


class GroupForm(forms.ModelForm):
    """
    Form for creating and editing Groups with selectable permissions.
    """
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select the permissions for this group."
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]
