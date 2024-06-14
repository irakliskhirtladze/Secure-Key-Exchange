from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Channel(models.Model):
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_channels',
                                    verbose_name=_('sender user'))
    recipient_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='received_channels', verbose_name=_('recipient user'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    accepted = models.BooleanField(default=False, verbose_name=_('accepted'))
    initial_sender_secret = models.TextField(null=True, blank=True, verbose_name=_('initial sender secret'))
    initial_recipient_secret = models.TextField(null=True, blank=True, verbose_name=_('initial recipient secret'))

    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('channels')

    def __str__(self):
        return self.name
