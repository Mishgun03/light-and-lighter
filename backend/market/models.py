from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    item_id = models.CharField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    archetype = models.CharField(max_length=255, null=True, blank=True)
    # rarity = models.CharField(max_length=255, db_index=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='favorites_by')

    class Meta:
        unique_together = ('user', 'item')
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user.username} - {self.item.name}'


class PriceHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='price_history')
    timestamp = models.DateTimeField()
    avg_price = models.FloatField()
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    volume = models.IntegerField()

    class Meta:
        ordering = ['-timestamp']
