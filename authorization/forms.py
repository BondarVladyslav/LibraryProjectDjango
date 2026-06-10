from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
class LoginForm(AuthenticationForm):
    username =  forms.CharField(label='Логин', widget=forms.TextInput())
    password =  forms.CharField(label='Пароль', widget=forms.PasswordInput())
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']




class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Пароль',widget=forms.PasswordInput())
    first_name = forms.CharField(label='Имя',widget=forms.TextInput())
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        labels={
            'username':'Имя',
            'email':"почта",
            'password1':'пароль',
            'password2':'Повторите пароль',
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email занят')
        return email
    

class UserProfile(forms.ModelForm):
    username = forms.CharField(disabled=True, widget=forms.TextInput())
    email = forms.CharField(disabled=True, widget=forms.TextInput())
    first_name = forms.CharField(label='Имя', widget=forms.TextInput())
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','first_name']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput())