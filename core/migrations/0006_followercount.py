# Generated by Django 5.0.8 on 2024-08-21 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
