# Generated by Django 4.2.16 on 2024-10-20 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_end',
            field=models.DateField(blank=True, null=True),
        ),
    ]
