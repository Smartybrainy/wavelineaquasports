from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

COUNTRY_CODE = (
    (234, 'Nigeria (+234)'),
    (233, 'Ghana (+233)')
)


class CustomSignupForm(UserCreationForm):
    password1 = forms.CharField(max_length=14, widget=forms.PasswordInput(attrs={
        'placeholder': "password",
        'class': 'form-control'
    }))
    password2 = forms.CharField(max_length=14, widget=forms.PasswordInput(attrs={
        'placeholder': "confirm password",
        'class': 'form-control'
    }))
    phone_number = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': "mobile mumber",
        'class': 'form-control'
    }))
    country_code = forms.ChoiceField(choices=COUNTRY_CODE, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': "full name",
        'class': 'form-control'
    }))
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': "email",
        'class': 'form-control'
    }))

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        for field_name in ['phone_number', 'country_code', 'full_name', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None
            self.fields[field_name].label = ''

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'country_code', 'full_name',
                  'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with same email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                _("Another user with this phone number already exists please try another"))
        return phone_number


class CustomLoginForm(forms.Form):
    # phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={
    #     'placeholder': 'mobile number',
    #     'class': 'form-control'
    # }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'email',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'password',
        'class': 'form-control mt-4'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].label = ''

    class Meta:
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError(
                "Sorry, your login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = authenticate(email=email, password=password)
            return user
        except:
            raise forms.ValidationError(
                _("Sorry, your login was invalid. Please try again."))


class PhoneVerificationForm(forms.Form):
    one_time_password = forms.IntegerField(label='')

    class Meta:
        help_texts = {'one_time_password': None}
        fields = ['one_time_password', ]


class PhoneVerificationForm(forms.Form):
    one_time_password = forms.IntegerField(label='')

    class Meta:
        help_texts = {'one_time_password': None}
        fields = ['one_time_password', ]


class CustomCreationForm(UserCreationForm):
    class Meta:
        class Meta(UserCreationForm.Meta):
            model = CustomUser
            fields = ('email',)


class CustomChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
