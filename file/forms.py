from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model  = Document
        fields = ['title', 'file','image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Fayl nomi...',
                'class': 'form-control'
            }),
        }