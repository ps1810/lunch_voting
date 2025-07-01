from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class DailyWinnerModel(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    restaurant = models.ForeignKey('restaurants.RestaurantModel', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=200)  # Denormalized for performance
    total_score = models.DecimalField(max_digits=6, decimal_places=2)
    unique_voters = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['restaurant']),
        ]

    def __str__(self):
        return f"{self.date}: {self.restaurant_name} (Score: {self.total_score})"