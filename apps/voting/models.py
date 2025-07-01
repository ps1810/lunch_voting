from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class VoteModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurants.RestaurantModel', related_name='votes', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['restaurant', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.restaurant.name} ({self.weight})"