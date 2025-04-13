from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.utils import timezone
from datetime import timedelta
from .serializers import RegistrationSerializer, LoginSerializer, TrainerRegistrationSerializer, CounsellorRegistrationSerializer
from .models import Student
from .utils.email import send_otp_email, send_new_otp_email
from .utils.messages import *



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class StudentRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.generate_otp()  # Generate OTP
            send_otp_email(user.email, user.otp)  # Send OTP email
            return Response({"message": USER_REGISTERED_SUCCESSFULLY}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = Student.objects.get(email=email)
            if user.otp == otp and user.otp_created_at > timezone.now() - timedelta(minutes=5):
                user.is_verified = True
                user.is_active = True
                user.otp = None
                user.otp_created_at = None
                user.save()
                return Response({"message": OTP_VERIFIED_SUCCESSFULLY}, status=status.HTTP_200_OK)
            else:
                return self.regenerate_otp(user)  # Regenerate OTP if invalid or expired
        except Student.DoesNotExist:
            return Response({"error": USER_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    def regenerate_otp(self, user):
        user.generate_otp()  # Generate a new OTP
        send_new_otp_email(user.email, user.otp)  # Send new OTP email
        return Response({"message": OTP_EXPIRED_MESSAGE}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_verified:
                    return Response({"error": ACCOUNT_INACTIVE}, status=status.HTTP_403_FORBIDDEN)
                tokens = get_tokens_for_user(user)  # Generate tokens
                return Response({
                    "tokens": tokens,
                    "message": LOGIN_SUCCESSFUL
                }, status=status.HTTP_200_OK)
            return Response({"error": INVALID_CREDENTIALS}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrainerRegistrationView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can access this view
    def post(self, request):
        serializer = TrainerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": TRAINER_REGISTERED_SUCCESSFULLY}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CounsellorRegistrationView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can access this view
    def post(self, request):
        serializer = CounsellorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": COUNSELLOR_REGISTERED_SUCCESSFULLY}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": REFRESH_TOKEN_REQUIRED}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": LOGOUT_SUCCESSFUL}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": INVALID_REFRESH_TOKEN}, status=status.HTTP_401_UNAUTHORIZED)
