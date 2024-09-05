from django.urls import path, include
from .views import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.auth_views import RegisterView, VerifyEmail

link_reducer_patterns = [
    path('shorten-url', views.shorten_url, name='shorten_url'),
    path('list-user-urls', views.get_all_urls, name='list_urls'),
    path('<str:short_url>', views.redirect_url, name='redirect_url'),
]

auth_patterns = [
    path('api/register/', RegisterView.as_view(), name='register'), # [ ] Potentiellement changer routes pour plus propre !
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify-email/', VerifyEmail.as_view(), name='verify_email'),
]

url_patterns = link_reducer_patterns + auth_patterns