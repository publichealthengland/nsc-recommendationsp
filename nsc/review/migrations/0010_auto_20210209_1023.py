# Generated by Django 2.2.11 on 2021-02-09 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0009_auto_20210205_1342"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalreview",
            name="stakeholders_confirmed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="review",
            name="stakeholders_confirmed",
            field=models.BooleanField(default=False),
        ),
    ]
