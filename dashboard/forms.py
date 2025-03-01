from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False, label='Staff Status')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data.get('is_staff', False)  # Ensure is_staff is correctly set

        if commit:
            user.save()
        return user

# Custom Login Form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    class Meta:
        fields = ['username', 'password']
