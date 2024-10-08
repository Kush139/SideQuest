# Generated by Django 5.0.8 on 2024-08-13 03:43

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_name_profile_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='post_images')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('num_of_likes', models.IntegerField(default=0)),
            ],
        ),
    ]
