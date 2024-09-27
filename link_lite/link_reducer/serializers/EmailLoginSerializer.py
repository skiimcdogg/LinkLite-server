from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(_('No user found with this email.'), code='authorization')
            
            user = authenticate(request=self.context.get('request'), username=user.username, password=password)
            
            if not user:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.'), code='authorization')
        else:
            raise serializers.ValidationError(_('Must include "email" and "password".'), code='authorization')
        
        attrs["user"] = user
        return attrs
