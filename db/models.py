from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Card(models.Model):
    artist = models.CharField(max_length=100)
    border = models.CharField(max_length=10, null=True)
    cmc = models.FloatField(null=True)
    color_identity = ArrayField(models.CharField(max_length=1, null=True), null=True)
    colors = ArrayField(models.CharField(max_length=5, null=True), null=True)
    flavor = models.TextField(max_length=1000, null=True)
    foreign_names = JSONField(null=True)
    hand = models.CharField(max_length=10, null=True)
    sdk_id = models.CharField(max_length=64, unique=True) #This is referred to as `id` in the SDK.
    image_url = models.URLField(max_length=200, null=True)
    layout = models.CharField(max_length=15, null=True)
    legalities = JSONField(null=True)
    life = models.CharField(max_length=10, null=True)
    loyalty = models.CharField(max_length=10, null=True)
    mana_cost = models.CharField(max_length=100, null=True)
    multiverse_id = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=255)
    names = ArrayField(models.CharField(max_length=255, null=True), null=True)
    number = models.CharField(max_length=10, null=True)
    original_text = models.TextField(max_length=1000, null=True)
    original_type = models.CharField(max_length=255, null=True)
    power = models.CharField(max_length=10, null=True)
    printings = ArrayField(models.CharField(max_length=10), null=True)
    rarity = models.CharField(max_length=50)
    release_date = models.DateField(null=True)
    rulings = JSONField(null=True)
    set = models.CharField(max_length=10)
    set_name = models.CharField(max_length=255)
    source = models.CharField(max_length=255, null=True)
    starter = models.BooleanField(null=True)
    subtypes = ArrayField(models.CharField(max_length=50), null=True)
    supertypes = ArrayField(models.CharField(max_length=20), null=True)
    text = models.TextField(max_length=1000, null=True)
    timeshifted = models.BooleanField(null=True)
    toughness = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=255)
    types = ArrayField(models.CharField(max_length=20), null=True)
    variations = ArrayField(models.CharField(max_length=64), null=True)
    watermark = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'card'
        verbose_name_plural = 'cards'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'card_detail',
            kwargs={
                'slug': slugify(self.name),
                'id': self.id,
            }
        )
        # return reverse('card_detail', args=[str(self.id)])

    def art_variations(self):
        if self.variations:
            return Card.objects.filter(
                sdk_id__in=[self.sdk_id, *self.variations]
                ).order_by('id')