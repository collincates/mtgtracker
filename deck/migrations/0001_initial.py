# Generated by Django 2.1.5 on 2019-02-03 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('db', '0024_auto_20190131_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=150)),
            ],
            options={
                'verbose_name': 'deck',
                'verbose_name_plural': 'decks',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DeckCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deckcards', to='db.Card')),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deckcards', to='deck.Deck')),
            ],
        ),
        migrations.AddField(
            model_name='deck',
            name='cards',
            field=models.ManyToManyField(related_name='decks', through='deck.DeckCard', to='db.Card'),
        ),
        migrations.AlterUniqueTogether(
            name='deckcard',
            unique_together={('card', 'deck')},
        ),
    ]
