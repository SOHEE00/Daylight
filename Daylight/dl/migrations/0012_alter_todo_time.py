# Generated by Django 5.0.3 on 2024-11-21 03:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dl", "0011_alter_todo_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="time",
            field=models.TimeField(default="00:00"),
        ),
    ]