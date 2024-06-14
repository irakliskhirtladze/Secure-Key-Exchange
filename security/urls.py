from django.urls import path, include
from rest_framework.routers import DefaultRouter
from security.views import ChannelViewSet, SecretExchangeView, KeyGenerationView

router = DefaultRouter()
router.register(r'channels', ChannelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('channels/<int:pk>/exchange/', SecretExchangeView.as_view(), name='secret-exchange'),
    path('channels/<int:pk>/generate-key/', KeyGenerationView.as_view(), name='key-generation'),
]
