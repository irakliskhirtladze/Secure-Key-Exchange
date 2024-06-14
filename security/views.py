import uuid
import os

from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from security.models import Channel
from security.serializers import ChannelSerializer, ChannelCreateSerializer, ChannelAcceptSerializer, EmptySerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ChannelCreateSerializer
        elif self.action == 'accept':
            return ChannelAcceptSerializer
        return ChannelSerializer

    def perform_create(self, serializer):
        recipient_user = serializer.validated_data['recipient_user']
        serializer.save(sender_user=self.request.user, recipient_user=recipient_user, name=str(uuid.uuid4()))

    def get_queryset(self):
        """
        Returns the list of Channels for the current user, where each user is part of the channel (sender or recipient).
        """
        user = self.request.user
        return Channel.objects.filter(sender_user=user) | Channel.objects.filter(recipient_user=user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        channel = self.get_object()
        if channel.recipient_user == request.user:
            channel.accepted = True
            channel.save()
            return Response({'status': 'channel accepted'})
        else:
            return Response({'status': 'not authorized'}, status=403)


class SecretExchangeView(APIView):
    """
    View to handle the exchange of secrets between users in a secure channel.

    This view allows each user (sender and recipient) in an accepted channel to
    post their secret. The secret is then used in key generation for secure communication.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def post(self, request, pk):
        # Fetch the channel using the provided primary key (pk)
        try:
            channel = Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            return Response({'status': 'channel not found'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is part of the channel and the channel is accepted
        if request.user not in [channel.sender_user, channel.recipient_user] or not channel.accepted:
            return Response({'status': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)

        # Generate a random secret key
        secret_key = int.from_bytes(os.urandom(32), byteorder='big')

        # Define the base and modulus for the secret exchange (assumed to be pre-defined in settings)
        base = int(settings.BASE)
        modulus = int(settings.MODULUS, 16)

        # Calculate and save the secret based on whether the user is the sender or recipient
        if request.user == channel.sender_user:
            channel.initial_sender_secret = pow(base, secret_key, modulus)
        elif request.user == channel.recipient_user:
            channel.initial_recipient_secret = pow(base, secret_key, modulus)

        channel.save()
        return Response({'secret_key': secret_key})


class KeyGenerationView(APIView):
    pass
