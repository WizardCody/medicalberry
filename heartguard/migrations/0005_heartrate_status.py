# Generated by Django 2.2.7 on 2020-01-10 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heartguard', '0004_auto_20200110_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='heartrate',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
