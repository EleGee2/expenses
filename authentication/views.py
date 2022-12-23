import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from validate_email import validate_email
from django.db.models import Q

from authentication.utils import send_activation_email, account_activation_token


# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        if not request.body:
            return JsonResponse({'message': "Please enter your username"})
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'error': "Username should only contain alphanumeric characters"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': "Username is already taken"}, status=409)
        return JsonResponse({'message': True})


class EmailValidationView(View):
    def post(self, request):
        if not request.body:
            return JsonResponse({'message': "Please enter your email"})
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'error': "This email is invalid"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': "Email is already been used"}, status=409)
        return JsonResponse({'message': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {'fieldValues': request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(
                    username=username,
                    email=email,
                )
                user.set_password(password)
                user.is_active = False
                user.save()

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                domain = get_current_site(request).domain
                link = reverse("activate", kwargs={'uid': uid, 'token': token})
                activate_url = 'https://' + domain + link

                send_activation_email({
                    'email': email,
                    'user': user,
                    'link': activate_url
                })

                messages.success(request, "Account created successfully")
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect("login")

            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully")
            return redirect("login")
        except Exception as e:
            pass

        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        if email and password:
            username = User.objects.get(Q(email__iexact=email)).username
            user = auth.authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' You are now logged in')
                    return redirect('expenses')

                messages.error(request, 'Account is not active, Please check your email')
                return render(request, 'authentication/login.html')

            messages.error(request, "Invalid email or password")
            return render(request, 'authentication/login.html')

        messages.warning(request, "Please input all fields")
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You are being logged out")
        return redirect("login")

