# Generated by Django 2.1.5 on 2019-01-29 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0020_auto_20190128_1615'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='collectioncards',
            unique_together={('card', 'collection')},
        ),
        migrations.AlterUniqueTogether(
            name='deckcards',
            unique_together={('card', 'deck')},
        ),
    ]
