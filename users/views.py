import random
import secrets
import string

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from config import settings
from users.forms import UserRegisterForm, UserForm, PermUserForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/user_register_form.html"
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения почты {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    characters = string.ascii_letters + string.digits
    new_password = ''.join(random.choice(characters) for i in range(12))
    send_mail(
        subject='Смена пароля',
        message=f'Новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('mailing:main'))


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_superuser=False)
        print(queryset)
        return queryset


class UserDetailView(PermissionRequiredMixin, DetailView):
    model = User
    permission_required = 'users.view_user'


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'users.user_delete'
    success_url = reverse_lazy('users:user_list')


class UserEditView(UpdateView):
    model = User
    success_url = reverse_lazy('users:user_list')
    form_class = PermUserForm

    def get_success_url(self):
        return reverse('users:user_view', args=[self.kwargs.get('pk')])
