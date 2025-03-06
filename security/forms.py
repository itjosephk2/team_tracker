from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from people_management.models import Person  # Adjust the import according to your project structure

class UserForm(forms.ModelForm):
    # Displayed only for new users to show the auto-generated password.
    password = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label="Generated Password",
        required=False
    )
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=True,
        label="Linked Person"
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'person']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            # For new users, auto-generate a random password.
            random_password = User.objects.make_random_password()
            self.fields['password'].initial = random_password
        else:
            # For existing users, remove the password field so it remains unchanged.
            self.fields.pop('password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        # Only update the password for new users.
        if not self.instance.pk:
            password = self.cleaned_data.get('password')
            user.set_password(password)
        if commit:
            user.save()
            person = self.cleaned_data.get('person')
            person.user = user
            person.save()
            # Only send an email when a new user is created.
            if not self.instance.pk:
                send_mail(
                    subject='Your Account Has Been Created',
                    message=f'Hello,\n\nYour account has been created. Your auto-generated password is: {self.cleaned_data.get("password")}',
                    from_email='noreply@yourdomain.com',  # Replace with your sender email.
                    recipient_list=[person.email],
                    fail_silently=False,
                )
        return user
