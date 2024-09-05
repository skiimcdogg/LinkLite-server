from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from ..serializers.auth_serializer   import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user).access_token
        send_mail(
            'Confirmez votre email',
            f'Cliquez sur ce lien pour confirmer votre email : http://localhost:8000/api/verify-email/?token={token}',  # [ ] !! à modifier et aussi pour prod
            'from@example.com',
            [user.email],
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
