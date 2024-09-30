from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Themes, Profile


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