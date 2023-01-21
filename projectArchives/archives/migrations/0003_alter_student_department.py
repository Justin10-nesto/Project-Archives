# Generated by Django 4.1.5 on 2023-01-21 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("archives", "0002_alter_student_regno"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="archives.department",
            ),
        ),
    ]
