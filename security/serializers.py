from rest_framework import serializers
from security.models import Channel
from django.contrib.auth import get_user_model


User = get_user_model()


class ChannelSerializer(serializers.ModelSerializer):
    sender_user = serializers.CharField(source='sender_user.email', read_only=True)
    recipient_user = serializers.CharField(source='recipient_user.email', read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'sender_user', 'recipient_user']


class ChannelCreateSerializer(serializers.ModelSerializer):
    recipient_user = serializers.CharField()

    class Meta:
        model = Channel
        fields = ['recipient_user']

    def validate_recipient_user(self, value):
        try:
            return User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Recipient user does not exist.")


class ChannelAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = []


class EmptySerializer(serializers.Serializer):
    """
    Serializer with no fields, used for endpoints that don't require input data.
    """
    pass
