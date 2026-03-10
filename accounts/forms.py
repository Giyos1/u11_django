from django import forms
from django.contrib.auth import authenticate
from accounts.models import VerificationCode, User
from common.service.email import send_email_in_thread


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


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=200)

    def save(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return None

        # 2) Yangi verification code yaratamiz
        code_obj = VerificationCode.objects.create(user=user)

        # 3) Emailga yuboramiz (thread orqali — sahifa kutmaydi)
        send_email_in_thread(
            subject="Parolni tiklash",
            message=f"Sizning kodingiz: {code_obj.code}\nKod 2 daqiqa ishlaydi.",
            recipient=user.email,
        )

        return code_obj


class ResetPasswordForm(forms.Form):
    code = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        code = self.cleaned_data['code']
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']

        if new_password != confirm_password:
            raise forms.ValidationError('ikkta password bir xil emas')

        try:
            code_obj = VerificationCode.objects.get(code=code)
        except VerificationCode.DoesNotExist:
            raise forms.ValidationError('sizning codingiz xato')

        if not code_obj.is_valid():
            raise forms.ValidationError('sizning codingiz xato')

        return self.cleaned_data

    def save(self):
        user = VerificationCode.objects.get(code=self.cleaned_data['code']).user
        user.set_password(self.cleaned_data['new_password'])
        user.save()
        return user
