from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, UserUpdateView, email_verification, generate_new_password, UserListView, \
    UserDetailView, UserDeleteView, UserEditView

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/new-password', generate_new_password, name='new-password'),

    path('user-list/', UserListView.as_view(), name='user_list'),
    path('client/<int:pk>', UserDetailView.as_view(), name='user_view'),
    path('user-delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
    path('user-manager-edit/<int:pk>', UserEditView.as_view(), name='user_manager_edit'),
]
