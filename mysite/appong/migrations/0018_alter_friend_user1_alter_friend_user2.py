# Generated by Django 5.1 on 2024-09-04 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appong', '0017_friend_user2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='user1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_friend1', to='appong.userprofile'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='user2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_friend2', to='appong.userprofile'),
        ),
    ]
