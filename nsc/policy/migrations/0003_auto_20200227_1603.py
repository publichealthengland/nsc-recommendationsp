# Generated by Django 2.2.9 on 2020-02-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("policy", "0002_auto_20200206_1043")]

    operations = [
        migrations.RemoveField(model_name="historicalpolicy", name="is_screened"),
        migrations.RemoveField(model_name="historicalpolicy", name="policy"),
        migrations.RemoveField(model_name="historicalpolicy", name="policy_html"),
        migrations.RemoveField(model_name="policy", name="is_screened"),
        migrations.RemoveField(model_name="policy", name="policy"),
        migrations.RemoveField(model_name="policy", name="policy_html"),
        migrations.AddField(
            model_name="historicalpolicy",
            name="recommendation",
            field=models.BooleanField(default=False, verbose_name="recommendation"),
        ),
        migrations.AddField(
            model_name="historicalpolicy",
            name="summary",
            field=models.TextField(default="", verbose_name="summary"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalpolicy",
            name="summary_html",
            field=models.TextField(default="", verbose_name="HTML summary"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="policy",
            name="recommendation",
            field=models.BooleanField(default=False, verbose_name="recommendation"),
        ),
        migrations.AddField(
            model_name="policy",
            name="summary",
            field=models.TextField(default="", verbose_name="summary"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="policy",
            name="summary_html",
            field=models.TextField(default="", verbose_name="HTML summary"),
            preserve_default=False,
        ),
    ]
