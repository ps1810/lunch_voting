from typing import List, Optional
from datetime import date
from core.entities.winner import DailyWinner
from core.repositories.winner import WinnerRepository
from apps.winners.models import DailyWinnerModel


class DjangoWinnerRepository(WinnerRepository):
    def get_by_date(self, target_date: date) -> Optional[DailyWinner]:
        try:
            model = DailyWinnerModel.objects.get(date=target_date)
            return self._to_entity(model)
        except DailyWinnerModel.DoesNotExist:
            return None

    def save(self, winner: DailyWinner) -> DailyWinner:
        model, created = DailyWinnerModel.objects.update_or_create(
            date=winner.date,
            defaults={
                'restaurant_id': winner.restaurant_id,
                'restaurant_name': winner.restaurant_name,
                'total_score': winner.total_score,
                'unique_voters': winner.unique_voters
            }
        )
        return self._to_entity(model)

    def get_date_range(self, start_date: Optional[date], end_date: Optional[date]) -> List[DailyWinner]:
        queryset = DailyWinnerModel.objects.all()

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return [self._to_entity(model) for model in queryset]

    def _to_entity(self, model: DailyWinnerModel) -> DailyWinner:
        return DailyWinner(
            date=model.date,
            restaurant_id=model.restaurant_id,
            restaurant_name=model.restaurant_name,
            total_score=model.total_score,
            unique_voters=model.unique_voters
        )