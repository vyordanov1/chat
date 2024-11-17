from django import forms
from django.contrib.auth.models import User, Group
from .models import Themes, Profile
from django.forms.widgets import ClearableFileInput
# from account.models import Admins
from chat.models import OffensiveWords, AbuseReport
import datetime



class HiddenImageInput(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['initial'] = None
        context['widget']['attrs']['class'] = 'hidden'
        context['widget']['attrs']['label'] = 'test'
        return context


class AbusingUserBaseForm(forms.Form):
    blocked_until = forms.DateTimeField(
        label='Block until',
        required=True,
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M:%S',
            attrs={'type': 'datetime-local'}
        ),
        input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S'],
    )


class BlockAbusingUserForm(AbusingUserBaseForm):
    pass


class OffensiveWordBaseForm(forms.ModelForm):
    class Meta:
        model = OffensiveWords
        fields = '__all__'


class OffensiveWordCreateForm(OffensiveWordBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['word'].label = ''

    word = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Add offensive word',
            }
        )
    )


class AbuseReportBaseForm(forms.ModelForm):
    class Meta:
        model = AbuseReport
        fields = '__all__'


class AbuseReportProcessForm(AbuseReportBaseForm):
    pass


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


# class EditUserForm(forms.ModelForm):
#     is_admin = forms.BooleanField(
#         required=False,
#         widget=forms.CheckboxInput,
#     )
#
#     class Meta:
#         model = Admins
#         fields = ('is_admin',)



class DismissAbuseForm(forms.ModelForm):
    def save(self, commit=True):
        report = super().save(commit=False)

        report.processed = True
        report.processed_date = datetime.datetime.now(tz=datetime.timezone.utc)

        if commit:
            report.save()

        return report

    class Meta:
        model = AbuseReport
        fields = ('processed', 'processed_date')
