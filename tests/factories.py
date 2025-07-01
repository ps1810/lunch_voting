import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from decimal import Decimal
from apps.restaurants.models import RestaurantModel
from apps.voting.models import VoteModel
from apps.winners.models import DailyWinnerModel


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = RestaurantModel

    name = factory.Faker("company")
    address = factory.Faker("address")
    phone = factory.Faker("phone_number")
    cuisine_type = factory.Faker("random_element", elements=["Italian", "Chinese", "Mexican", "Indian"])


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = VoteModel

    user = factory.SubFactory(UserFactory)
    restaurant = factory.SubFactory(RestaurantFactory)
    weight = factory.Faker("random_element", elements=[Decimal("1.0"), Decimal("0.5"), Decimal("0.25")])


class DailyWinnerFactory(DjangoModelFactory):
    class Meta:
        model = DailyWinnerModel

    date = factory.Faker("date")
    restaurant = factory.SubFactory(RestaurantFactory)
    restaurant_name = factory.LazyAttribute(lambda obj: obj.restaurant.name)
    total_score = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    unique_voters = factory.Faker("random_int", min=1, max=50)