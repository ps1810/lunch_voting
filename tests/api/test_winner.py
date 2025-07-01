from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from freezegun import freeze_time
from tests.factories import UserFactory, RestaurantFactory, VoteFactory

class WinnerViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.client.force_authenticate(user=self.user1)

    @freeze_time("2025-06-30")
    def test_calculate_winner(self):
        restaurant1 = RestaurantFactory()
        restaurant2 = RestaurantFactory()

        # Create votes for restaurant1 (higher score)
        VoteFactory(restaurant=restaurant1, weight=1.0, user=self.user1)
        VoteFactory(restaurant=restaurant1, weight=0.5, user=self.user1)

        # Create vote for restaurant2 (lower score)
        VoteFactory(restaurant=restaurant2, weight=1.0, user=self.user2)

        response = self.client.get('/api/winners/today/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['restaurant_id'], restaurant1.id)
        self.assertEqual(float(response.data['total_score']), 1.5)

    @freeze_time("2025-06-30")
    def test_calculate_winner_with_equal_score(self):
        restaurant1 = RestaurantFactory()
        restaurant2 = RestaurantFactory()

        # Create votes for restaurant1 (higher score)
        VoteFactory(restaurant=restaurant1, weight=1.0, user=self.user1)
        VoteFactory(restaurant=restaurant1, weight=0.5, user=self.user1)
        VoteFactory(restaurant=restaurant1, weight=0.25, user=self.user1)
        VoteFactory(restaurant=restaurant1, weight=0.25, user=self.user1)

        # Create vote for restaurant2 (lower score)
        VoteFactory(restaurant=restaurant2, weight=1.0, user=self.user2)
        VoteFactory(restaurant=restaurant2, weight=1.0, user=self.user1)

        response = self.client.get('/api/winners/today/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['restaurant_id'], restaurant2.id)
        self.assertEqual(float(response.data['total_score']), 2.0)