from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from .models import Student, Trainer


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs
    def create(self, validated_data):
        user = Student(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            is_active=False  # Set inactive until verified
        )
        user.set_password(validated_data['password'])
        user.save()
        user.generate_otp()  # Generate OTP
        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {user.otp}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class TrainerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['expertise']

class CounsellorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['expertise']