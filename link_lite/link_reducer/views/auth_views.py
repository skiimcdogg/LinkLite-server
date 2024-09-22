from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from ..serializers.auth_serializer   import RegisterSerializer


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user).access_token
        verification_link = f"{settings.FRONTEND_URL}/verify-email?token={str(token)}" # [ ] Rajouter Lien front dans settings
        
        send_mail(
            'Confirmez votre email',
            f'Cliquez sur ce lien pour confirmer votre email : {verification_link}',
            'from@example.com',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({'detail': 'Vérifiez votre email pour confirmer votre inscription.'}, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        try:
            user_id = RefreshToken(token).get('user_id')
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response({'detail': 'Email confirmé avec succès.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Lien de confirmation invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user

        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })