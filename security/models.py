from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from cryptography.fernet import Fernet


class Channel(models.Model):
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_channels',
                                    verbose_name=_('sender user'))
    recipient_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='received_channels', verbose_name=_('recipient user'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    accepted = models.BooleanField(default=False, verbose_name=_('accepted'))
    initial_sender_secret = models.TextField(null=True, blank=True, verbose_name=_('initial sender secret'))
    initial_recipient_secret = models.TextField(null=True, blank=True, verbose_name=_('initial recipient secret'))
    sender_secret_key = models.TextField(null=True, blank=True, verbose_name=_('sender secret key'))
    recipient_secret_key = models.TextField(null=True, blank=True, verbose_name=_('recipient secret key'))

    class Meta:
        verbose_name = _('channel')
        verbose_name_plural = _('channels')

    def __str__(self):
        return self.name

    @staticmethod
    def encrypt_secret_key(secret_key):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        return fernet.encrypt(secret_key.to_bytes((secret_key.bit_length() + 7) // 8, byteorder='big')).decode()

    @staticmethod
    def decrypt_secret_key(encrypted_secret_key):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        return int.from_bytes(fernet.decrypt(encrypted_secret_key.encode()), byteorder='big')
