# Generated by Django 3.1.3 on 2020-11-19 04:19
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('song_id', models.AutoField(primary_key=True, serialize=False)),
                ('song_artist', models.CharField(default='', max_length=50)),
                ('song_title', models.CharField(default='', max_length=50)),
                ('song_text', models.TextField(default='')),
            ],
        )
    ]
