from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        widgets = {'password': forms.PasswordInput()}

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('ikkta password bir xil emas')
        return self.cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('email'), password=data.get('password'))

        if not user:
            raise forms.ValidationError('username yoki parrol xato')

        return {'user': user}
