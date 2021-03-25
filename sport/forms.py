from django import forms
from .models import Contact


class ContactEnquiriesForm(forms.ModelForm):
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                                   "id": "name",
                                   "placeholder": "your name*"
                               }))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "id": "email",
            "placeholder": "your email*"
        }))
    phone = forms.CharField(max_length=16, widget=forms.NumberInput(
        attrs={
            # "type": "number",
            "class": "form-control",
            "id": "phone",
            "placeholder": "enter your phone number*"
        }))
    message = forms.CharField(max_length=1500, widget=forms.Textarea(attrs={
        'rows': 5,
        'cols': 'auto',
        "class": "form-control",
        "id": "message",
        "placeholder": "your message*"
    }))

    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'message')
