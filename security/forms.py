from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from people_management.models import Person  # Adjust the import according to your project structure


class UserForm(forms.ModelForm):
    # Auto-generated password field. Displayed as plain text and readonly.
    password = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label="Generated Password",
        required=False
    )
    # Field to link a user to a Person. This field is required.
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=True,
        label="Linked Person"
    )

    class Meta:
        model = User
        # Removed email, first_name, and last_name from the fields.
        fields = ['username', 'password', 'person']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For new users, auto-generate a random password.
        if not self.instance.pk:
            random_password = User.objects.make_random_password()
            self.fields['password'].initial = random_password

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
        # Set the password using the auto-generated value.
        password = self.cleaned_data.get('password')
        user.set_password(password)
        if commit:
            user.save()
            # Associate the user with the selected Person.
            # (Adjust this logic based on your Person model's relationship to User.)
            person = self.cleaned_data.get('person')
            # For example, if Person has a OneToOneField to User:
            person.user = user
            person.save()
            
            # Now, send an email to the user's email (pulled from the Person instance).
            # Ensure you have configured your email settings in settings.py.
            send_mail(
                subject='Your Account Has Been Created',
                message=f'Hello,\n\nYour account has been created. Your auto-generated password is: {password}',
                from_email='noreply@yourdomain.com',  # Replace with your sender email.
                recipient_list=[person.email],
                fail_silently=False,
            )
        return user
