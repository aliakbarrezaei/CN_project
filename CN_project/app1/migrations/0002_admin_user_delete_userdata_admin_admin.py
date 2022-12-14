# Generated by Django 4.0.6 on 2022-08-01 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Y', 'not confirmed'), ('N', 'confirmed')], default='N', help_text='Register status', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Y', 'striked'), ('N', 'non-striked')], default='N', help_text='Strike status', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserData',
        ),
        migrations.AddField(
            model_name='admin',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app1.user'),
        ),
    ]
