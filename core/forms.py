from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class BookingForm(forms.Form):
    GROUP_SIZE_CHOICES = [
        (1, '1 Explorer'),
        (2, '2 Explorers'),
        (3, '3 Explorers'),
        (4, '4 Explorers'),
        (5, '5+ Private Group'),
    ]

    full_name = forms.CharField(
        max_length=200,
        required=True,
        error_messages={'required': 'Please enter your full name.'},
    )
    travel_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'required': 'Please select a travel date.'},
    )
    group_size = forms.ChoiceField(
        choices=GROUP_SIZE_CHOICES,
        required=True,
    )


class QuickBookingForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your Full Name'})
    )
    phone_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'WhatsApp / Phone'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Tour preference or details...', 'rows': 1})
    )
    
    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        # Simple cleaning if needed
        return data
