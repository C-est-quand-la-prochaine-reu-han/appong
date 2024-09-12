# Generated by Django 5.1 on 2024-09-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appong', '0006_rename_tournament_id_match_tournament'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='tourn_creator',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='tourn_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='tourn_start_time',
            new_name='start_time',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='tourn_confirmed',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='tourn_pending',
        ),
        migrations.AddField(
            model_name='tournament',
            name='confirmed',
            field=models.ManyToManyField(blank=True, related_name='conf', to='appong.userprofile'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='pending',
            field=models.ManyToManyField(blank=True, related_name='pend', to='appong.userprofile'),
        ),
    ]
