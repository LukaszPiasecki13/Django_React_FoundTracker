from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api-auth/', include('rest_framework.urls')),


    #OLD
    # path('register/', views.RegistrationView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('validate-username/', csrf_exempt(views.UserNameValidationView.as_view()), name='validate-username'),
    # path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email')

]
