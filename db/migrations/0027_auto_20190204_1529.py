# Generated by Django 2.1.5 on 2019-02-04 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0026_auto_20190204_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expansionset',
            name='slug',
            field=models.SlugField(max_length=150, unique=True),
        ),
    ]
