# Generated by Django 5.1 on 2024-09-06 13:30

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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_nick', models.CharField(max_length=30)),
                ('avatar', models.ImageField(default='default_avatar.jpg', upload_to='')),
                ('friends_confirmed', models.ManyToManyField(blank=True, to='appong.userprofile')),
                ('friends_pending', models.ManyToManyField(blank=True, to='appong.userprofile')),
                ('friends_remove', models.ManyToManyField(blank=True, to='appong.userprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tourn_start_time', models.DateTimeField(auto_now_add=True)),
                ('tourn_name', models.CharField(max_length=30)),
                ('tourn_confirmed', models.ManyToManyField(blank=True, related_name='tourn_conf', to='appong.userprofile')),
                ('tourn_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appong.userprofile')),
                ('tourn_pending', models.ManyToManyField(blank=True, related_name='tourn_pend', to='appong.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_start_time', models.DateTimeField(auto_now_add=True)),
                ('match_end_time', models.DateTimeField(auto_now=True)),
                ('player1_hit_nb', models.PositiveIntegerField(default=0)),
                ('player2_hit_nb', models.PositiveIntegerField(default=0)),
                ('player1_perfect_hit_nb', models.PositiveIntegerField(default=0)),
                ('player2_perfect_hit_nb', models.PositiveIntegerField(default=0)),
                ('player1_score', models.PositiveIntegerField(default=0)),
                ('player2_score', models.PositiveIntegerField(default=0)),
                ('ball_max_speed', models.PositiveIntegerField(default=0)),
                ('match_status', models.PositiveIntegerField(default=0)),
                ('tournament_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournament', to='appong.tournament')),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='appong.userprofile')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='appong.userprofile')),
            ],
        ),
    ]
