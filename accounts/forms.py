from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import check_password

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name",
                  "email"]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name",
                  "email"]


class UserLoginModelForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': "Email"}),
        required=True
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': "Senha"}),
        required=True
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Não existe usuário com esse email.')
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = CustomUser.objects.get(email=email)
        print("CHECAGEM" + str(check_password(password, user.password)))
        if not check_password(password, user.password):
            raise forms.ValidationError('Senha incorreta.')
        return password

class UserRegisterModelForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirmar Senha', widget=forms.PasswordInput)
    username = forms.CharField(
        label="Nome de usuario",
        required=True
    )
    firstname = forms.CharField(
        label="Primeiro nome",
        required=True
    )
    lastname = forms.CharField(
        label="Sobrenome",
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'firstname', 'lastname',
                  'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("O email já existe")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "As senhas não estão iguais")
        return cleaned_data
