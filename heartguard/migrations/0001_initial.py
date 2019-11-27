# Generated by Django 2.2.7 on 2019-11-24 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('MAC_address', models.CharField(max_length=17)),
            ],
        ),
        migrations.CreateModel(
            name='Heartrate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=0, max_digits=3)),
                ('event_time', models.DateTimeField(verbose_name='time of event')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heartguard.Device')),
            ],
        ),
    ]