from .views import (CustomSignupView,
                    CustomLoginView,
                    # phone_verification_view
                    activate,
                    )

from django.contrib import messages
from django.urls import path
from django.contrib.auth import views as auth_views
from django.dispatch import receiver
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed
)
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

app_name = "accounts"


@receiver(user_logged_in, sender=CustomUser)
def user_logged_in_info(sender, user, request, **kwargs):
    if user:
        msg = "Successfully logged in {user}.".format(
            user=request.user)
    else:
        msg = "Logged in successfully"
    messages.add_message(request, messages.INFO, msg)


@receiver(user_logged_out, sender=CustomUser)
def user_logout_in_info(sender, user, request, **kwargs):
    if user:
        msg = f"{user} logged out."
    else:
        msg = "Logged out successfully"
    messages.add_message(request, messages.INFO, msg)


@receiver(user_login_failed, sender=CustomUser)
def user_login_failed_info(sender, user, request, **kwargs):
    if user:
        msg = "Sorry, your login was invalid. Please try again.!"
    else:
        msg = "Invalid credentials!"
    messages.add_message(request, messages.WARNING, msg)


urlpatterns = [
    path('signup/', CustomSignupView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    # path('verify/', phone_verification_view, name="verify"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # For reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(
         template_name="registration/password_reset.html"
         ),
         name="password-reset"),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="registration/password_reset_done.html"
         ),
         name="password-reset-done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="registration/password_reset_confirm.html"
         ),
         name="password-reset-comfirm"),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="registration/password_reset_complete.html"
         ),
         name="password-reset-complete"),
]
