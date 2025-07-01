from datetime import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.use_cases.restaurant_use_cases import RestaurantUseCases
from infrastructure.repositories.django_restaurant import DjangoRestaurantRepository
from .serializers import RestaurantSerializer, RestaurantUpdateSerializer
from rest_framework.decorators import action
import logging

logger = logging.getLogger(__name__)


class RestaurantViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restaurant_repo = DjangoRestaurantRepository()
        self.use_cases = RestaurantUseCases(self.restaurant_repo)

    def list(self, request):
        restaurants = self.use_cases.get_all_restaurants()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            restaurant = self.use_cases.create_restaurant(
                id=None,
                name=serializer.validated_data['name'],
                address=serializer.validated_data.get('address', ''),
                phone=serializer.validated_data.get('phone', ''),
                cuisine_type=serializer.validated_data.get('cuisine_type', ''),
                is_votable=serializer.validated_data.get('is_votable', True)
            )
            response_serializer = RestaurantSerializer(restaurant)
            logger.info(f"Created restaurant: {restaurant.name}")
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to create restaurant: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        restaurant = self.use_cases.get_restaurant(int(pk))
        if restaurant:
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data)
        return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        restaurant = self.use_cases.get_restaurant(int(pk))
        if not restaurant:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RestaurantUpdateSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            updated_restaurant = self.use_cases.create_restaurant(
                id=restaurant.id,
                name=serializer.validated_data.get('name', restaurant.name),
                address=serializer.validated_data.get('address', restaurant.address),
                phone=serializer.validated_data.get('phone', restaurant.phone),
                cuisine_type=serializer.validated_data.get('cuisine_type', restaurant.cuisine_type),
                is_votable=serializer.validated_data.get('is_votable', restaurant.is_votable)
            )
            response_serializer = RestaurantSerializer(updated_restaurant)
            logger.info(f"Updated restaurant: {updated_restaurant.name} by {request.user.username}")
            return Response(response_serializer.data)
        logger.error(f"Failed to update restaurant: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if self.use_cases.delete_restaurant(int(pk)):
            logger.info(f"Deleted restaurant with ID: {pk} by {request.user.username}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        logger.error(f"Failed to delete restaurant with ID: {pk} as there is no restaurant with that ID")
        return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search restaurants by name, cuisine, or address"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter q is required'}, status=status.HTTP_400_BAD_REQUEST)

        restaurants = self.use_cases.search_restaurants(query)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def votable(self, request):
        """Get restaurants that the current user can still vote for today"""
        restaurants = self.use_cases.get_voteable_restaurants()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)