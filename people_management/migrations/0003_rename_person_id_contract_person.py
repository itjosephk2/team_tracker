# Generated by Django 4.2.16 on 2024-10-20 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people_management', '0002_alter_contract_contract_end'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='person_id',
            new_name='person',
        ),
    ]
