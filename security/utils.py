from rest_framework import status
from rest_framework.response import Response
from security.models import Channel


def get_channel_and_validate_user(request, pk):
    """
    Utility function to fetch a channel and validate the current user.
    """
    # Fetch the channel using the provided primary key (pk)
    try:
        channel = Channel.objects.get(pk=pk)
    except Channel.DoesNotExist:
        return None, Response({'status': 'channel not found'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure the user is part of the channel and the channel is accepted
    if request.user not in [channel.sender_user, channel.recipient_user] or not channel.accepted:
        return None, Response({'status': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)

    return channel, None
