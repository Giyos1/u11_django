from django import forms
from post.models import Post


class PostForms(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title_uz',
            'content_uz',
            'title_en',
            'content_en',
        ]
