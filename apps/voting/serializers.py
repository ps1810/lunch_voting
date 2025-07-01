from rest_framework import serializers

class VoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    restaurant_id = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

class VoteCreateSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()

class UserVoteStatsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    date = serializers.DateField()
    votes_used = serializers.IntegerField()
    votes_remaining = serializers.IntegerField()
    total_allowed = serializers.IntegerField()