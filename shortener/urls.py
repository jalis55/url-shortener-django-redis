from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.ShortenerAPIView.as_view(), name='api_home'),
    path('api/shorten/', views.ShortenerAPIView.as_view(), name='shorten_url'),
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),
]