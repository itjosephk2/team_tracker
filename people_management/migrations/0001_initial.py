# Generated by Django 4.2.16 on 2024-10-20 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255)),
                ('phone_number', models.IntegerField()),
                ('date_of_birth', models.DateField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('contract_start', models.DateField()),
                ('contract_end', models.DateField()),
                ('hourly_rate', models.FloatField(default=12.45)),
                ('contracted_hours', models.FloatField(default=40)),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people_management.person')),
            ],
        ),
    ]