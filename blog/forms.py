from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'placeholder': 'type here...',
        'class': 'form-control',
        'id': 'exampleInputEmail1',
        'rows': '3',
        'cols': 'auto',
        'aria-describedby': 'comment'
    }))
    author = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'author',
        'aria-describedby': 'author'
    }))

    class Meta:
        model = Comment
        fields = ('author', 'content')
