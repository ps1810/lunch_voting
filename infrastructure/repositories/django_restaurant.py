from typing import List, Optional
from django.db.models import Q
from core.entities.restaurant import Restaurant
from core.repositories.restaurant import RestaurantRepository
from apps.restaurants.models import RestaurantModel


class DjangoRestaurantRepository(RestaurantRepository):
    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        try:
            model = RestaurantModel.objects.get(id=restaurant_id)
            return self._to_entity(model)
        except RestaurantModel.DoesNotExist:
            return None

    def get_all(self) -> List[Restaurant]:
        models = RestaurantModel.objects.all()
        return [self._to_entity(model) for model in models]

    def save(self, restaurant: Restaurant) -> Restaurant:
        if restaurant.id:
            # Update existing
            model = RestaurantModel.objects.get(id=restaurant.id)
            model.name = restaurant.name
            model.address = restaurant.address
            model.phone = restaurant.phone
            model.cuisine_type = restaurant.cuisine_type
            model.is_votable = restaurant.is_votable
            model.save()
        else:
            # Create new
            model = RestaurantModel.objects.create(
                name=restaurant.name,
                address=restaurant.address,
                phone=restaurant.phone,
                cuisine_type=restaurant.cuisine_type,
            )

        return self._to_entity(model)

    def delete(self, restaurant_id: int) -> bool:
        try:
            RestaurantModel.objects.get(id=restaurant_id).delete()
            return True
        except RestaurantModel.DoesNotExist:
            return False

    def search(self, query: str) -> List[Restaurant]:
        models = RestaurantModel.objects.filter(
            Q(name__icontains=query) |
            Q(cuisine_type__icontains=query) |
            Q(address__icontains=query)
        )
        return [self._to_entity(model) for model in models]

    def get_votable_restaurants(self) -> List[Restaurant]:
        """Get restaurants the user can still vote for today."""
        models = RestaurantModel.objects.filter(is_votable=True)
        return [self._to_entity(model) for model in models]

    def _to_entity(self, model: RestaurantModel) -> Restaurant:
        return Restaurant(
            id=model.id,
            name=model.name,
            address=model.address,
            phone=model.phone,
            cuisine_type=model.cuisine_type,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_votable=model.is_votable
        )