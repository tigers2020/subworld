from django import forms

from .models import Subtitle


class SubtitleForm(forms.ModelForm):
    class Meta:
        model = Subtitle
        fields = ("user", "title", 'sub_file', 'language', 'resolution', 'rip', 'release', 'author', 'comment')
        widgets = {
            'user': forms.HiddenInput()
            
        }