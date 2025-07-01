from rest_framework import serializers

class DailyWinnerSerializer(serializers.Serializer):
    date = serializers.DateField()
    restaurant_id = serializers.IntegerField()
    restaurant_name = serializers.CharField()
    total_score = serializers.DecimalField(max_digits=6, decimal_places=2)
    unique_voters = serializers.IntegerField()