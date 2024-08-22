# Generated by Django 5.1 on 2024-08-22 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appong', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='friends_confirmed',
            field=models.ManyToManyField(default=None, related_name='friend_conf', to='appong.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='friends_pending',
            field=models.ManyToManyField(default=None, related_name='friend_pend', to='appong.userprofile'),
        ),
    ]
