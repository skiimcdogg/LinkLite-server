from django.urls import path, include
from .views import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views.auth_views import RegisterView, VerifyEmail, LogoutView, UserDetailView, EmailLoginView

link_reducer_patterns = [
    path('csrf-token/', views.get_csrf_token, name='csrf_token'),
    path('shorten-url/', views.shorten_url, name='shorten_url'),
    path('list-user-urls/', views.get_all_urls_from_user, name='list_urls'),
    path('<str:short_url>/', views.redirect_url, name='redirect_url'),
    path('delete-url/<str:short_url>/', views.delete_url, name='redirect_url'),
]

auth_patterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', EmailLoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify-email/', VerifyEmail.as_view(), name='verify_email'),
    path('api/user/', UserDetailView.as_view(), name='user-detail'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns = link_reducer_patterns + auth_patterns