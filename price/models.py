from django.db import models
from db.models import Card


class Price(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='prices'
    )
    vendor = models.ForeignKey(
        'Vendor',
        on_delete=models.CASCADE,
        related_name='prices'
    )
    condition = models.ForeignKey(
        'Condition',
        on_delete=models.CASCADE,
        related_name='prices'
    )
    timestamp = models.DateTimeField()
    qty_in_stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['card', 'vendor', 'condition', 'timestamp']),
        ]
        unique_together = ('card', 'vendor', 'condition', 'timestamp',)
        verbose_name = 'price'
        verbose_name_plural = 'prices'

    def __str__(self):
        return self.price


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'vendor'
        verbose_name_plural = 'vendors'

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'condition'
        verbose_name_plural = 'conditions'

    def __str__(self):
        return self.name
