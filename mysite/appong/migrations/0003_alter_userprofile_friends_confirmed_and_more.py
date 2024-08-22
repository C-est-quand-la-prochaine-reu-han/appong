# Generated by Django 5.1 on 2024-08-22 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appong', '0002_alter_userprofile_friends_confirmed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='friends_confirmed',
            field=models.ManyToManyField(blank=True, related_name='friend_conf', to='appong.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='friends_pending',
            field=models.ManyToManyField(blank=True, related_name='friend_pend', to='appong.userprofile'),
        ),
    ]
