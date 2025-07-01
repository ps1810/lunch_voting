from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from freezegun import freeze_time
from datetime import date
from tests.factories import UserFactory, RestaurantFactory, VoteFactory


class VoteViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.restaurant = RestaurantFactory()

    @freeze_time("2025-06-30")
    def test_create_vote(self):
        data = {"restaurant_id": self.restaurant.id}

        response = self.client.post('/api/votes/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['restaurant_id'], self.restaurant.id)
        self.assertEqual(response.data['weight'], 1.0)  # First vote

    @freeze_time("2025-06-30")
    def test_create_second_vote(self):
        data = {"restaurant_id": self.restaurant.id}

        response = self.client.post('/api/votes/', data)
        response = self.client.post('/api/votes/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['restaurant_id'], self.restaurant.id)
        self.assertEqual(response.data['weight'], 0.5)

    @freeze_time("2025-06-30")
    def test_create_subsequent_vote(self):
        data = {"restaurant_id": self.restaurant.id}

        response = self.client.post('/api/votes/', data)
        response = self.client.post('/api/votes/', data)
        response = self.client.post('/api/votes/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['restaurant_id'], self.restaurant.id)
        self.assertEqual(response.data['weight'], 0.25)

    @freeze_time("2025-06-30")
    def test_maximum_vote(self):
        data = {"restaurant_id": self.restaurant.id}

        response = self.client.post('/api/votes/', data)
        response = self.client.post('/api/votes/', data)
        response = self.client.post('/api/votes/', data)
        response = self.client.post('/api/votes/', data)
        response = self.client.post('/api/votes/', data)
        response = self.client.post('/api/votes/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Daily vote limit of 5 reached")
