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
    sdk_id = models.CharField(max_length=64, unique=True) #This is referred to as `id` in the SDK.
    set = models.CharField(max_length=10)
    set_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150, null=False, unique=True)
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
        ordering = ('name',)
        verbose_name = 'card'
        verbose_name_plural = 'cards'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Initial save to populate ID column
        super(Card, self).save(*args, **kwargs)
        # Create a slug with format 'id-cardname'
        self.slug = slugify(f'{self.id}-{self.name}')
        # Update slug field only
        super(Card, self).save(update_fields=['slug'])

    def get_absolute_url(self):
        return reverse('db:card_detail', kwargs={'card_slug': self.slug})

    def art_variations(self):
        if self.variations:
            return Card.objects.filter(
                sdk_id__in=[self.sdk_id, *self.variations]
                ).values_list('slug', flat=True).order_by('id')


class ExpansionSet(models.Model):
    booster = JSONField(null=True)
    border = models.CharField(max_length=10, null=True)
    block = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=10, unique=True)
    gatherer_code = models.CharField(max_length=10, null=True)
    magic_cards_info_code = models.CharField(max_length=10, null=True)
    mkm_id = models.CharField(max_length=10, null=True)
    mkm_name = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=255)
    old_code = models.CharField(max_length=10, null=True)
    online_only = models.BooleanField(null=True)
    release_date = models.CharField(max_length=10)
    slug = models.SlugField(max_length=150, null=False, unique=True)
    type = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ('release_date',)
        verbose_name = 'set'
        verbose_name_plural = 'sets'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Initial save to populate ID column
        super(ExpansionSet, self).save(*args, **kwargs)
        # Create a slug with format 'expansion-set-name'
        self.slug = slugify(f'{self.name}')
        # Update slug field only
        super(ExpansionSet, self).save(update_fields=['slug'])

    def get_absolute_url(self):
        return reverse('db:set_detail', kwargs={'set_slug': self.slug})

    # def generate_random_booster(self):
    #     pass
