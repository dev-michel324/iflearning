from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, SCHOOL_GRADE


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name",
                  "email", "birth", "school_grade"]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name",
                  "email", "birth", "school_grade"]


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
    birth = forms.DateField(
        label="Data de nascimento",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
    )

    school_grade = forms.ChoiceField(
        label="Grau escolar",
        choices=SCHOOL_GRADE
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'firstname', 'lastname',
                  'email', 'birth', 'school_grade']

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
