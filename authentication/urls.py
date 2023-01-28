from .views import *
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uid>/<token>', VerificationView.as_view(), name='activate'),
    path('password-reset-link', PasswordResetLink.as_view(), name="password-reset-link"),
    path('set-new-password/<uid>/<token>', CompletePasswordReset.as_view(), name='reset-user-password'),
]
