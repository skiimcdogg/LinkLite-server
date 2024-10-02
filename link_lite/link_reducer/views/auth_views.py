import logging
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from ..serializers.RegisterSerializer import RegisterSerializer
from ..serializers.EmailLoginSerializer import EmailLoginSerializer

logger = logging.getLogger(__name__)


class EmailLoginView(generics.GenericAPIView):
    serializer_class = EmailLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        verification_link = f"{settings.FRONTEND_URL}/email-verification?token={str(token)}" # [ ] Rajouter Lien front dans settings
        
        send_mail(
            'Confirmez votre email',
            f'Cliquez sur ce lien pour confirmer votre email : {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({'detail': 'Vérifiez votre email pour confirmer votre inscription.'}, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        try:
            user_id = RefreshToken(token).get('user_id')
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response({'detail': 'Email confirmé avec succès.'}, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError) as e:
            logger.error(f"Invalid token: {str(e)}")
            return Response({'error': 'Le token est invalide ou mal formé.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error("User not found.")
            return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Lien de confirmation invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })