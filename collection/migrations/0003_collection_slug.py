# Generated by Django 2.1.5 on 2019-02-09 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20190203_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='slug',
            field=models.SlugField(default='none', max_length=150),
            preserve_default=False,
        ),
    ]
