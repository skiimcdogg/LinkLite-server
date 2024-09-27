from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)


    class Meta:
        model = User
        fields = ('first_name', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This account already exists.")
        return value

    def create(self, validated_data):
        first_name = validated_data['first_name']
        username = first_name.lower()

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False  
        user.save()
        return user
