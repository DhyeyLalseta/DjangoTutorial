# Generated by Django 3.0.8 on 2020-07-07 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200703_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
