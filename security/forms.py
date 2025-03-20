import secrets
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from people_management.models import Person


class CustomUserCreationForm(UserCreationForm):
    """
    Form for admins to create a new user and link them to a Person.
    
    Features:
    - Only allows selecting employees (Persons) who are not already linked to a user.
    - Optionally assigns the user to a group.
    - Generates a secure password and emails the user.
    """

    person = forms.ModelChoiceField(
        queryset=Person.objects.filter(user__isnull=True),  # Only show unlinked persons
        required=True,
        label="Select Employee",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Assign Permissions Group",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email"]  # Removed password fields since it is autogenerated
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}),
        }
        help_texts = {"username": ""}

    def __init__(self, *args, **kwargs):
        """Dynamically set the person queryset to include the currently linked person."""
        super().__init__(*args, **kwargs)
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)

    def clean_username(self):
        """Ensure the username is unique."""
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_person(self):
        """Ensure the selected person is not already linked to another user."""
        person = self.cleaned_data.get("person")
        if person and person.user:
            raise forms.ValidationError("This person is already linked to another user.")
        return person

    def save(self, commit=True):
        """
        Creates a new user, links them to the selected Person, 
        assigns a group (if selected), and sends login credentials via email.
        """
        user = forms.ModelForm.save(self, commit=False)
        person = self.cleaned_data.get("person")

        # Copy personal details from Person to User
        user.first_name = person.first_name
        user.last_name = person.last_name
        user.email = person.email

        # Generate and set a secure random password
        random_password = secrets.token_urlsafe(12)
        user.set_password(random_password)

        if commit:
            user.save()
            person.user = user  # Link the Person model to this User
            person.save()

            # Assign group if selected
            group = self.cleaned_data.get("group")
            if group:
                user.groups.add(group)

            # Send email with login credentials
            send_mail(
                "Your New Account Credentials",
                f"Hello {user.first_name},\n\nYour account has been created.\n"
                f"Username: {user.username}\nPassword: {random_password}\n\n"
                "Please log in and change your password.",
                "admin@yourdomain.com",
                [user.email],
                fail_silently=False,
            )

        return user


class CustomUserUpdateForm(forms.ModelForm):
    """
    Form for updating user details and managing their link to a Person.
    
    Features:
    - Allows changing email and username.
    - Allows linking/unlinking a Person.
    - Assigns the user to a group.
    """

    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    person = forms.ModelChoiceField(
        queryset=Person.objects.filter(user__isnull=True), 
        required=False,
        label="Link to Employee",
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
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        """Dynamically set the person queryset to include the currently linked person."""
        super().__init__(*args, **kwargs)
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)


        if self.instance and hasattr(self.instance, "person"):
            linked_person = self.instance.person 

            if linked_person:
                self.fields["person"].queryset = Person.objects.filter(
                    user__isnull=True
                ) | Person.objects.filter(id=linked_person.id)

                # Preselect the currently linked person
                self.fields["person"].initial = linked_person

    def save(self, commit=True):
        """
        Updates the user, handles linking/unlinking a Person, and assigns a group.
        
        Rules enforced:
        - Users can switch to another Person.
        - Users can be unlinked from a Person.
        - A Person can only be linked to ONE user.
        - A User can only have ONE Person linked.
        """
        user = super().save(commit=False)
        selected_person = self.cleaned_data.get("person")
        group = self.cleaned_data.get("group")

        # Check if the user is already linked to a Person
        try:
            current_person = user.person  # Get the currently linked person
        except Person.DoesNotExist:
            current_person = None

        # Handle unlinking (if dropdown is blank)
        if current_person and not selected_person:
            current_person.user = None
            current_person.save()

        # Handle linking or switching to a different person
        elif selected_person and selected_person != current_person:
            # Ensure the new person is not already linked to another user
            if selected_person.user and selected_person.user != user:
                raise forms.ValidationError("This person is already linked to another user. Unlink first.")

            # Unlink previous person (if exists)
            if current_person:
                current_person.user = None
                current_person.save()

            # Link the selected person
            selected_person.user = user
            selected_person.save()

        # Assign or update group
        if group:
            user.groups.set([group])  # Replace existing groups with the selected group

        if commit:
            user.save()

        return user


class CustomLoginForm(AuthenticationForm):
    """Custom login form extending Django's default authentication form."""
    pass


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
