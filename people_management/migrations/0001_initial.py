# Generated by Django 4.2.16 on 2025-03-06 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import people_management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('security', '0002_remove_role_is_default_alter_role_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('date_of_birth', models.DateField()),
                ('active', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_members', to='people_management.person')),
                ('role', models.ForeignKey(blank=True, default=people_management.models.get_default_role, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='people', to='security.role')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('contract_start', models.DateField()),
                ('contract_end', models.DateField(blank=True, null=True)),
                ('hourly_rate', models.FloatField(default=12.45)),
                ('contracted_hours', models.FloatField(default=40)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='people_management.person')),
            ],
        ),
    ]
