# Generated by Django 4.0.6 on 2022-08-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_rename_dislike_video_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='unavailable_videos_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='label',
            field=models.CharField(choices=[('L', 'limited'), ('U', 'unlimited')], default='U', help_text='label status', max_length=1),
        ),
        migrations.AddField(
            model_name='video',
            name='status',
            field=models.CharField(choices=[('A', 'accessible'), ('I', 'inaccessible')], default='A', help_text='Video status', max_length=1),
        ),
        migrations.AlterField(
            model_name='admin',
            name='status',
            field=models.CharField(choices=[('N', 'not confirmed'), ('C', 'confirmed')], default='N', help_text='Register status', max_length=1),
        ),
        migrations.AlterField(
            model_name='users',
            name='status',
            field=models.CharField(choices=[('S', 'striked'), ('N', 'non-striked')], default='N', help_text='Strike status', max_length=1),
        ),
    ]
