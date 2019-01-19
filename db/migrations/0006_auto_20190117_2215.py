# Generated by Django 2.1.5 on 2019-01-18 06:15

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_auto_20190117_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='foreign_names',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='hand',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='layout',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='legalities',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='life',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='loyalty',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='mana_cost',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='multiverse_id',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, null=True), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='original_text',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='original_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='power',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='release_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='rulings',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='source',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='starter',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='subtypes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='card',
            name='supertypes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='card',
            name='text',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='timeshifted',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='toughness',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='types',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='card',
            name='watermark',
            field=models.CharField(max_length=50, null=True),
        ),
    ]