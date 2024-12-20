# Generated by Django 5.0.3 on 2024-11-30 07:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dl", "0013_alter_todo_time"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_name", models.CharField(max_length=20)),
                ("user_email", models.EmailField(max_length=254, unique=True)),
                ("user_password", models.CharField(max_length=100)),
                ("user_validate", models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name="todo",
            name="time",
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 30, 0, 0)),
        ),
    ]
