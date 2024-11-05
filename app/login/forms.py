import uuid

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PasswordReset
import logging

logger = logging.getLogger(__name__)


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-input',
                'required': '',
                'name': 'username',
                'id': 'username',
                'type': 'text',
                'placeholder': 'John Doe',
                'maxlength': '25',
                'minlength': '6',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-input',
                'required': '',
                'name': 'email',
                'id': 'email',
                'type': 'text',
                'placeholder': 'johndoe@gmail.com',
                'maxlength': '254',
                'minlength': '6',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'class': 'form-input',
                'required': '',
                'name': 'password1',
                'id': 'password1',
                'type': 'password',
                'placeholder': 'password',
                'maxlength': '254',
                'minlength': '6',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'class': 'form-input',
                'required': '',
                'name': 'password2',
                'id': 'password2',
                'type': 'password',
                'placeholder': 'confirm password',
                'maxlength': '254',
                'minlength': '6',
            }
        )

    username = forms.CharField(max_length=25)
    email = forms.EmailField(required=True, max_length=254, widget=
                             forms.EmailInput(
                                 attrs={
                                     'type': 'text'
                                 }
                             ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PasswordResetForm(forms.Form):
    username = forms.CharField(
        max_length=25,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'name': 'username',
                'id': 'username',
                'type': 'text',
                'placeholder': 'John Doe',

            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'name': 'email',
                'id': 'email',
                'type': 'text',
                'placeholder': 'johndoe@gmail.com',
            }
        )
    )

    def clean(self):
        """
        Overwriting the clean method to make sure the
        correct user and email are typed in before
        allowing password reset
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username and email:
            try:
                user = User.objects.get(
                    username=username,
                    email=email,
                )
                self.cleaned_data['user_id'] = user.id
            except User.DoesNotExist:
                raise forms.ValidationError(
                    "There is no such username with matching email"
                )
        return cleaned_data


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(
        label='Enter Password',
        max_length=254,
        min_length=6,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'name': 'password1',
                'id': 'password1',
                'type': 'password',
                'placeholder': 'password',
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm password',
        max_length=254,
        min_length=6,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'name': 'password2',
                'id': 'password2',
                'type': 'password',
                'placeholder': 'confirm password',
            }
        )
    )

    def clean(self):
        """
        Overwriting the clean method to
        compare if both passwords match
        before changing it
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return cleaned_data

