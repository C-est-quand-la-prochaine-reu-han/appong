# Generated by Django 5.1 on 2024-09-04 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appong', '0016_remove_friend_user2'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='user2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='appong.userprofile'),
        ),
    ]
