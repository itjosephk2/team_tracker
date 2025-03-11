from django import forms
from django.contrib.auth.models import User
from people_management.models import Person  # Ensure correct import
from security.models import Role, PermissionDefinition


# User Form
class UserForm(forms.ModelForm):
    """
    Form for creating and updating users with a linked 'Person' model.
    """
    person = forms.ModelChoiceField(
        queryset=Person.objects.none(),  # Initially empty, dynamically set in __init__
        required=True,
        label="Link Employee",
        widget=forms.Select(attrs={"class": "form-control"})  # Bootstrap
    )

    class Meta:
        model = User
        fields = ["username", "person"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}),
        }
        help_texts = {
            "username": "",  # Remove default Django help text
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the currently linked Person object, if it exists
        current_person = None
        if self.instance.pk:  # Check if we're editing an existing user
            current_person = Person.objects.filter(user=self.instance).first()

        # Query for persons who are either:
        # - Not linked to any user
        # - Already linked to this specific user
        queryset = Person.objects.filter(user__isnull=True)
        if current_person:
            queryset |= Person.objects.filter(pk=current_person.pk)

        self.fields["person"].queryset = queryset

        # Preselect the currently linked employee (if any)
        if current_person:
            self.fields["person"].initial = current_person

    def clean_username(self):
        """
        Ensure the username is unique.
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_person(self):
        """
        Ensure the selected person is not already linked to another user.
        """
        person = self.cleaned_data.get("person")
        if person and person.user and person.user != self.instance:
            raise forms.ValidationError("This person is already linked to another user.")
        return person

    def save(self, commit=True):
        """
        Save the user and associate it with a Person instance.
        """
        user = super().save(commit=False)
        if commit:
            user.save()
            person = self.cleaned_data.get("person")
            person.user = user
            person.save()
        return user


# Role Form
class RoleForm(forms.ModelForm):
    """
    Form for managing roles and assigning permissions.
    """
    permissions = forms.ModelMultipleChoiceField(
        queryset=PermissionDefinition.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),  # Bootstrap checkboxes
        required=False
    )

    class Meta:
        model = Role
        fields = ["name", "description", "permissions"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter role name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter role description"}),
        }

    def clean_name(self):
        """
        Prevent renaming predefined roles.
        """
        name = self.cleaned_data.get("name")
        if self.instance.pk and self.instance.name in Role.PREDEFINED_ROLES and self.instance.name != name:
            raise forms.ValidationError("This role name is reserved and cannot be changed.")
        return name

    def save(self, commit=True):
        """
        Save the role and update associated permissions.
        """
        role = super().save(commit=False)
        if commit:
            role.save()
            self.cleaned_data["permissions"].set(role.permissions.all())
        return role
