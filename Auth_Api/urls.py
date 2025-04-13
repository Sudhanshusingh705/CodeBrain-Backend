from django.urls import path
from .views import StudentRegistrationView,TrainerRegistrationView, LoginView, CounsellorRegistrationView, LogoutView,VerifyOtpView


urlpatterns = [
    path('register-student/', StudentRegistrationView.as_view(), name='register-student'),
    path('register-trainer/', TrainerRegistrationView.as_view(), name='register-trainer'),
    path('register-counsellor/', CounsellorRegistrationView.as_view(), name='register-counsellor'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]