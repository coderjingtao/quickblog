from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','url','text') # displayed on pages
        
        # add placeholder to displayed attributes
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            #'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'url': forms.TextInput(attrs={'placeholder': 'URL'}),
            'text': forms.Textarea(attrs={'placeholder': 'Comment'}),
        }
        