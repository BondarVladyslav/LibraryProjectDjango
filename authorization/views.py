from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ChangePasswordForm, LoginForm, RegisterForm, UserProfileChangeData

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = "authorization/login.html"

class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'authorization/register.html'
    success_url = reverse_lazy('authorization:login')

class UserChangeDataView(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    form_class = UserProfileChangeData
    template_name = 'authorization/change_my_data.html'
    def get_success_url(self):
        return reverse_lazy('authorization:change_data')
    
    def get_object(self, queryset=None):
        return self.request.user
    

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'authorization/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'authorization/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('authorization:change_data')
