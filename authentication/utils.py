from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


def send_activation_email(data):
    user = data["user"]
    link = data["link"]
    subject = "Activate your account"
    body = "Hi " + user.username + ' ' + \
           'Please use this link to verify your account\n' + link
    email = EmailMessage(
        subject,
        body,
        'noreply@expenses.com',
        [data["email"]],
    )

    return email.send(fail_silently=False)


def send_password_reset_email(data):
    user = data["user"]
    link = data["link"]
    subject = "Reset your password"
    body = "Hi " + user.username + ' ' + \
           'Please use this link below to reset your password\n' + link
    email = EmailMessage(
        subject,
        body,
        'noreply@expenses.com',
        [data["email"]],
    )

    return email.send(fail_silently=False)


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


account_activation_token = AppTokenGenerator()
