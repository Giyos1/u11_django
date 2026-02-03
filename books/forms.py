from django import forms

from books.models import Genre, Book


def musbat(value):
    if value < 0:
        raise forms.ValidationError('0 dan katta son kiriting')


class BookForm(forms.Form):
    title = forms.CharField(max_length=255, label='title')
    description = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'placeholder': 'description toldiring'}
    ))
    page_count = forms.IntegerField()
    price = forms.DecimalField(max_digits=6, decimal_places=2, validators=[musbat])
    genre = forms.ChoiceField(choices=Genre)


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'price', 'page_count', 'genre', 'author']

    def clean_title(self):
        if len(self.cleaned_data.get('title')) < 5:
            raise forms.ValidationError(' 5 ta harfdan koproq title yoz')
        return self.cleaned_data.get('title')

    def clean(self):
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        if title == description:
            raise forms.ValidationError('ikkalsi bir xil bolmasin')
        return self.cleaned_data
