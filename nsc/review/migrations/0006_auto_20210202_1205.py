# Generated by Django 2.2.11 on 2021-02-02 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stakeholder', '0001_initial'),
        ('review', '0005_auto_20210202_1155'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReviewNotification',
            new_name='ReviewStakeholderNotification',
        ),
    ]
