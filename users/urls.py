from django.urls import path, reverse_lazy
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    # Account Credentials
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html",
                                                redirect_authenticated_user=True), name="login"),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html",
                                               success_url=reverse_lazy("password_change_done")),
         name="password_change"),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html"),
        name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete")),
        name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_complete.html"),
        name="password_reset_complete"),

    path('watchlist/', views.watchlist, name='watchlist'),
    path('preferences/', views.preferences, name='preferences'),
    path('developers/', views.developers, name='developers'),
    path('settings/', views.settings, name='settings'),
    path('delete_account/', views.delete_account, name='delete_account'),
]
