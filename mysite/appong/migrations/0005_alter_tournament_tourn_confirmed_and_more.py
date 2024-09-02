# Generated by Django 5.1 on 2024-09-02 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appong', '0004_alter_match_tournament_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='tourn_confirmed',
            field=models.ManyToManyField(blank=True, related_name='tourn_conf', to='appong.userprofile'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='tourn_pending',
            field=models.ManyToManyField(blank=True, related_name='tourn_pend', to='appong.userprofile'),
        ),
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
