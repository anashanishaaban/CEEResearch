# Generated by Django 5.1.3 on 2024-11-21 20:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboardapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PointCloudFile",
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
                ("name", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="pointclouds/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name="Message",
        ),
    ]