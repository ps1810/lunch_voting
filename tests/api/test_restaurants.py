from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from tests.factories import UserFactory, RestaurantFactory


class RestaurantViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # self.user = UserFactory()
        # self.client.force_authenticate(user=self.user)

    def test_create_restaurant(self):
        data = {
            "name": "New Restaurant",
            "cuisine_type": "Italian",
            "address": "123 Test St"
        }

        response = self.client.post('/api/restaurants/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Restaurant")
        self.assertEqual(response.data['cuisine_type'], "Italian")

    def test_list_restaurants(self):
        RestaurantFactory.create_batch(3)

        response = self.client.get('/api/restaurants/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_restaurant(self):
        restaurant = RestaurantFactory()

        response = self.client.get(f'/api/restaurants/{restaurant.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], restaurant.name)

    def test_update_restaurant(self):
        restaurant = RestaurantFactory()
        data = {"name": "Updated Name", "is_votable": False}

        response = self.client.put(f'/api/restaurants/{restaurant.id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Name")
        self.assertEqual(response.data['is_votable'], False)

    def test_delete_restaurant(self):
        restaurant = RestaurantFactory()

        response = self.client.delete(f'/api/restaurants/{restaurant.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_restaurants(self):
        RestaurantFactory(name="Pizza Palace")
        RestaurantFactory(name="Burger King")

        response = self.client.get('/api/restaurants/search/?q=pizza')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("Pizza", response.data[0]['name'])