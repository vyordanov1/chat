from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Themes, Profile

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


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={
            'class': 'form-input',
            'name': 'first_name',
            'id': 'first_name',
            'type': 'text',
            'placeholder': 'John',
        }
    ))
    last_name = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={
            'class': 'form-input',
            'name': 'last_name',
            'id': 'last_name',
            'type': 'text',
            'placeholder': 'Doe',
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ThemeForm(forms.ModelForm):
    name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'name': 'name',
                'id': 'name',
                'type': 'text',
                'placeholder': 'dark/light',
            }
        )
    )

    class Meta:
        model = Themes
        fields = ('name',)


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=254,
        label='',
        required=False,
        widget=forms.TextInput(
            attrs= {
                "placeholder": "Search",
            }
        )
    )
