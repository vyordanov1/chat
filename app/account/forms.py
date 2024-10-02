import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Themes, Profile
from chat.models import ChatRoom
from django.forms.widgets import ClearableFileInput
from account.models import Admins


class HiddenImageInput(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['initial'] = None
        context['widget']['attrs']['class'] = 'hidden'
        context['widget']['attrs']['label'] = 'test'
        return context


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


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=ClearableFileInput(
            attrs={
                'onchange': 'handleFileUpload(event)'
            }
        )
    )

    class Meta:
        model = Profile
        fields = ('image',)


class EditUserForm(forms.ModelForm):
    is_admin = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Admins
        fields = ('is_admin',)

