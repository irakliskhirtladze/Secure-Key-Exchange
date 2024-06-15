import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from security.models import Channel

User = get_user_model()


class ChannelAPITests(APITestCase):

    def setUp(self):
        self.sender = User.objects.create_user(email='sender@example.com', password='k3NoXc!&jc')
        self.recipient = User.objects.create_user(email='recipient@example.com', password='k3NoXc!&jc')

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_channel_creation_and_acceptance(self):
        """
        Test the creation and acceptance process of a channel.
        """
        self.authenticate(self.sender)
        url = reverse('channel-list')
        data = {
            'recipient_user': self.recipient.email
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        channel_id = response.data['id']

        # Accept the channel as the recipient
        self.authenticate(self.recipient)
        url = reverse('channel-accept', kwargs={'pk': channel_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the channel is accepted
        channel = Channel.objects.get(id=channel_id)
        self.assertTrue(channel.accepted)

    def test_secret_exchange_and_key_generation(self):
        """
        Test the secret exchange and key generation processes.
        """
        self.authenticate(self.sender)
        channel = Channel.objects.create(
            sender_user=self.sender,
            recipient_user=self.recipient,
            name=str(uuid.uuid4()),
            accepted=True
        )
        channel_id = channel.id

        # Perform secret exchange as the sender
        url = reverse('secret-exchange', kwargs={'pk': channel_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sender_secret_key = response.data['secret_key']
        channel.refresh_from_db()
        self.assertIsNotNone(channel.initial_sender_secret)

        # Perform secret exchange as the recipient
        self.authenticate(self.recipient)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipient_secret_key = response.data['secret_key']
        channel.refresh_from_db()
        self.assertIsNotNone(channel.initial_recipient_secret)

        # Generate shared key as the sender
        self.authenticate(self.sender)
        url = reverse('key-generation', kwargs={'pk': channel_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sender_shared_key = response.data['shared_key']

        # Generate shared key as the recipient
        self.authenticate(self.recipient)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipient_shared_key = response.data['shared_key']

        # Ensure the shared keys match
        self.assertEqual(sender_shared_key, recipient_shared_key)
