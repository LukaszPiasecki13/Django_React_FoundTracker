from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from authentication.models import UserProfile
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]










# class UserNameValidationView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         username = data['username']
#         if not str(username).isalnum():
#             return JsonResponse({'username_error': 'username can not contain special characters'}, status=400)
#         # if User.objects.filter(username=username).exists():
#         #     return JsonResponse({'username_error': 'username already exists, choose another one'}, status=409)

#         return JsonResponse({'username_valid': True})


# class EmailValidationView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         email = data['email']
#         if not validate_email(email):
#             return JsonResponse({'email_error': 'Emial is invalid'}, status=400)
#         if UserProfile.objects.filter(email=email).exists():
#             return JsonResponse({'email_error': 'email already exists, choose another one'}, status=409)

#         return JsonResponse({'email_valid': True})


# class RegistrationView(View):
#     def get(self, request):
#         return render(request, 'authentication/register.html')

#     def post(self, request):
#         # Get user data
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         context = {
#             'fieldValue': request.POST
#         }

#         if not UserProfile.objects.filter(username=username).exists():
#             if not UserProfile.objects.filter(email=email).exists():
#                 if len(password) < 6:
#                     messages.error(request, 'Password too short. Need 6 marks')
#                     return render(request, 'authentication/register.html', context)

#                 user = UserProfile.objects.create_user(username=username, email=email)
#                 user.set_password(password)
#                 user.save()
#                 messages.success(request, 'Account created successfully')
#                 return render(request, 'authentication/login.html')

#             messages.error(request, 'Email already exists')
#             return render(request, 'authentication/register.html')

#         messages.error(request, 'Username already exists')
#         return render(request, 'authentication/register.html')

# class LoginView(View):
#     def get(self, request):
#         return render(request, 'authentication/login.html')

#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']

#         user = auth.authenticate(username=username, password=password)

#         if user:
#             auth.login(request, user)
#             messages.success(request, 'Welcome, ' + user.username + '. You are now logged in')
#             return redirect('main_dashboard')

#         messages.error(request, 'Invalid credentials, try again')
#         return render(request, 'authentication/login.html')


# class LogoutView(View):
#     def get(self, request):
#         auth.logout(request)
#         messages.success(request, 'You have been logged out')
#         return redirect('login')