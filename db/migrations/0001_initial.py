# Generated by Django 2.1.5 on 2019-01-18 00:34

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('border', models.CharField(max_length=10)),
                ('cmc', models.FloatField()),
                ('color_identity', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), size=None)),
                ('colors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5), size=None)),
                ('flavor', models.TextField(max_length=1000)),
                ('foreign_names', django.contrib.postgres.fields.jsonb.JSONField()),
                ('hand', models.CharField(max_length=10)),
                ('sdk_id', models.CharField(max_length=64)),
                ('image_url', models.URLField(unique=True)),
                ('layout', models.CharField(max_length=15)),
                ('legalities', django.contrib.postgres.fields.jsonb.JSONField()),
                ('life', models.CharField(max_length=10)),
                ('loyalty', models.CharField(max_length=10)),
                ('mana_cost', models.CharField(max_length=100)),
                ('multiverse_id', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('number', models.CharField(max_length=10)),
                ('original_text', models.TextField(max_length=1000)),
                ('original_type', models.CharField(max_length=255)),
                ('power', models.CharField(max_length=10)),
                ('printings', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), size=None)),
                ('rarity', models.CharField(max_length=50)),
                ('release_date', models.DateField()),
                ('rulings', django.contrib.postgres.fields.jsonb.JSONField()),
                ('set', models.CharField(max_length=10)),
                ('set_name', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('starter', models.BooleanField()),
                ('subtypes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
                ('supertypes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None)),
                ('text', models.TextField(max_length=1000)),
                ('timeshifted', models.BooleanField()),
                ('toughness', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=255)),
                ('types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=None)),
                ('variations', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), size=None)),
                ('watermark', models.CharField(max_length=50)),
            ],
        ),
    ]
