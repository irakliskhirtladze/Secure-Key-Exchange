# Generated by Django 5.0.6 on 2024-06-14 12:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('accepted', models.BooleanField(default=False, verbose_name='accepted')),
                ('initial_sender_secret', models.TextField(blank=True, null=True, verbose_name='initial sender secret')),
                ('initial_recipient_secret', models.TextField(blank=True, null=True, verbose_name='initial recipient secret')),
                ('recipient_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_channels', to=settings.AUTH_USER_MODEL, verbose_name='recipient user')),
                ('sender_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_channels', to=settings.AUTH_USER_MODEL, verbose_name='sender user')),
            ],
            options={
                'verbose_name': 'channel',
                'verbose_name_plural': 'channels',
            },
        ),
    ]
