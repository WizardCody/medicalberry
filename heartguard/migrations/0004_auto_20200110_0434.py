# Generated by Django 2.2.7 on 2020-01-10 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heartguard', '0003_device_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='max_heartrate',
            field=models.DecimalField(decimal_places=0, default=75, max_digits=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='min_heartrate',
            field=models.DecimalField(decimal_places=0, default=50, max_digits=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='notify_mail',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='notify_telegram',
            field=models.BooleanField(default=True),
        ),
    ]
