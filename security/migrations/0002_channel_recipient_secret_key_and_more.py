# Generated by Django 5.0.6 on 2024-06-15 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='recipient_secret_key',
            field=models.TextField(blank=True, null=True, verbose_name='recipient secret key'),
        ),
        migrations.AddField(
            model_name='channel',
            name='sender_secret_key',
            field=models.TextField(blank=True, null=True, verbose_name='sender secret key'),
        ),
    ]
