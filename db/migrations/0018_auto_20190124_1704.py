# Generated by Django 2.1.5 on 2019-01-25 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0017_auto_20190124_1626'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='deckcards',
            unique_together={('deck', 'card')},
        ),
    ]
