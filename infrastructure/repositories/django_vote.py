from typing import List
from datetime import date
from core.entities.vote import Vote, RestaurantVoteStats
from core.repositories.vote import VoteRepository
from apps.voting.models import VoteModel
from django.db.models import Count, Sum
class DjangoVoteRepository(VoteRepository):
    def get_user_votes_for_date(self, user_id: int, target_date: date) -> List[Vote]:
        models = VoteModel.objects.filter(
            user_id=user_id,
            created_at__date=target_date
        )
        return [self._to_entity(model) for model in models]

    def get_user_votes_for_restaurant_for_date(self, user_id: int, restaurant_id: int, target_date: date) -> List[Vote]:
        models = VoteModel.objects.filter(
            user_id=user_id,
            restaurant_id=restaurant_id,
            created_at__date=target_date
        )
        return [self._to_entity(model) for model in models]

    def get_restaurant_votes_for_date(self, restaurant_id: int, target_date: date) -> List[Vote]:
        models = VoteModel.objects.filter(
            restaurant_id=restaurant_id,
            created_at__date=target_date
        )
        return [self._to_entity(model) for model in models]

    def save(self, vote: Vote) -> Vote:
        model = VoteModel.objects.create(
            user_id=vote.user_id,
            restaurant_id=vote.restaurant_id,
            weight=vote.weight
        )
        return self._to_entity(model)

    def user_has_voted_for_restaurant(self, user_id: int, restaurant_id: int, target_date: date) -> bool:
        return VoteModel.objects.filter(
            user_id=user_id,
            restaurant_id=restaurant_id,
            created_at__date=target_date
        ).exists()

    def get_all_votes_for_date(self, target_date: date) -> List[Vote]:
        models = VoteModel.objects.filter(created_at__date=target_date)
        return [self._to_entity(model) for model in models]

    def get_votes_of_restaurants_for_date(self, target_date: date) -> List[RestaurantVoteStats]:
        stats = (
            VoteModel.objects.filter(created_at__date=target_date)
            .values('restaurant_id','restaurant__name')
            .annotate(
                total_votes=Count('id'),
                unique_voters=Count('user_id', distinct=True),
                total_score=Sum('weight')
            )
        )

        return [
            RestaurantVoteStats(
                restaurant_id=stat['restaurant_id'],
                restaurant_name=stat['restaurant__name'],
                date=target_date,
                total_votes=stat['total_votes'],
                unique_voters=stat['unique_voters'],
                total_score=stat['total_score'] or 0
            ) for stat in stats
        ]

    def _to_entity(self, model: VoteModel) -> Vote:
        return Vote(
            id=model.id,
            user_id=model.user_id,
            restaurant_id=model.restaurant_id,
            weight=model.weight,
            created_at=model.created_at
        )