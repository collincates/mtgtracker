# Generated by Django 2.1.7 on 2019-02-21 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0029_auto_20190216_2226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ('id',), 'verbose_name': 'card', 'verbose_name_plural': 'cards'},
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
