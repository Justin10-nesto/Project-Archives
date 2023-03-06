# Generated by Django 3.2 on 2023-02-17 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0013_auto_20230217_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archives.document'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archives.staff'),
        ),
    ]