# Generated by Django 3.2.13 on 2022-06-21 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("robin", "0001_initial"),
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
                ("login", models.CharField(max_length=64)),
                ("email", models.CharField(max_length=64)),
                ("password", models.CharField(max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
