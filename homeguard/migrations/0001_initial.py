# Generated by Django 2.2.7 on 2020-01-09 21:37

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
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Kontrakton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(default=False)),
                ('event_time', models.DateTimeField(verbose_name='time of event')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeguard.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Gas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('event_time', models.DateTimeField(verbose_name='time of event')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeguard.Device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeguard.DeviceType'),
        ),
    ]
