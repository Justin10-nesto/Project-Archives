# Generated by Django 3.2 on 2023-02-17 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0014_auto_20230217_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='progress',
            old_name='project',
            new_name='document',
        ),
    ]
