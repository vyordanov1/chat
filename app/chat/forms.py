from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

