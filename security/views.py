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
from security.utils import get_channel_and_validate_user


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
        """
        Handles the creation of a new channel.
        """
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
        """
        Handles the acceptance of a channel by the recipient.
        """
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

    @staticmethod
    def post(request, pk):
        channel, error_response = get_channel_and_validate_user(request, pk)
        if error_response:
            return error_response

        # Generate a random secret key
        secret_key = int.from_bytes(os.urandom(32), byteorder='big')

        base = int(settings.BASE)
        modulus = int(settings.MODULUS, 16)

        # Calculate and save the secret based on whether the user is the sender or recipient
        encrypted_secret_key = channel.encrypt_secret_key(secret_key)
        if request.user == channel.sender_user:
            channel.initial_sender_secret = pow(base, secret_key, modulus)
            channel.sender_secret_key = encrypted_secret_key
        elif request.user == channel.recipient_user:
            channel.initial_recipient_secret = pow(base, secret_key, modulus)
            channel.recipient_secret_key = encrypted_secret_key

        channel.save()
        return Response({'secret_key': secret_key})


class KeyGenerationView(APIView):
    """
    View to handle the generation of the shared key between users in a secure channel.

    This view computes the final shared key using the secrets exchanged between
    the sender and recipient in an accepted channel.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @staticmethod
    def post(request, pk):
        channel, error_response = get_channel_and_validate_user(request, pk)
        if error_response:
            return error_response

        # Ensure both secrets have been exchanged
        if channel.initial_sender_secret is None or channel.initial_recipient_secret is None:
            return Response({'status': 'secrets not fully exchanged'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the stored secret key from database
        if request.user == channel.sender_user:
            secret_key = channel.decrypt_secret_key(channel.sender_secret_key)
        elif request.user == channel.recipient_user:
            secret_key = channel.decrypt_secret_key(channel.recipient_secret_key)

        if secret_key is None:
            return Response({'status': 'secret_key not found for user'}, status=status.HTTP_400_BAD_REQUEST)

        # Compute the shared key using the recipient's secret and the stored secret key
        if request.user == channel.sender_user:
            shared_key = pow(int(channel.initial_recipient_secret), secret_key, int(settings.MODULUS, 16))
        elif request.user == channel.recipient_user:
            shared_key = pow(int(channel.initial_sender_secret), secret_key, int(settings.MODULUS, 16))

        return Response({'shared_key': shared_key})
