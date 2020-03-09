# Generated by Django 2.2.9 on 2020-03-09 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0003_remove_review_policies"),
        ("policy", "0004_merge_20200302_0847"),
    ]

    operations = [
        migrations.AddField(
            model_name="policy",
            name="reviews",
            field=models.ManyToManyField(
                related_name="policies", to="review.Review", verbose_name="reviews"
            ),
        )
    ]
