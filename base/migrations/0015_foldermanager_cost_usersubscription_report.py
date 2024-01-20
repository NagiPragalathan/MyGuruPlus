# Generated by Django 4.1.9 on 2024-01-20 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("base", "0014_foldermanager_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="foldermanager",
            name="cost",
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name="UserSubscription",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("is_premium", models.CharField(max_length=255)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("message", models.TextField(max_length=255)),
                ("question_id", models.IntegerField()),
                ("flag", models.CharField(max_length=50)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
