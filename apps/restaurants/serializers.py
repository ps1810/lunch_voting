from rest_framework import serializers

class RestaurantSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    cuisine_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_votable = serializers.BooleanField(read_only=True)

class RestaurantCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    address = serializers.CharField(required=False, allow_blank=True, default='')
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')
    cuisine_type = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')

class RestaurantUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    cuisine_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    is_votable = serializers.BooleanField(required=False)