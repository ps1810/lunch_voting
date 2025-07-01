from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import datetime
from core.use_cases.winner_use_cases import WinnerUseCases
from infrastructure.repositories.django_restaurant import DjangoRestaurantRepository
from infrastructure.repositories.django_vote import DjangoVoteRepository
from infrastructure.repositories.django_winner import DjangoWinnerRepository
from .serializers import DailyWinnerSerializer
import logging

logger = logging.getLogger(__name__)


class WinnerViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vote_repo = DjangoVoteRepository()
        self.restaurant_repo = DjangoRestaurantRepository()
        self.winner_repo = DjangoWinnerRepository()
        self.winner_use_cases = WinnerUseCases(self.vote_repo, self.restaurant_repo, self.winner_repo)

    def list(self, request):
        """Get historical winners with optional date filtering"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        start_date_obj = None
        end_date_obj = None

        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                logger.error(f"Invalid start_date format: {start_date}")
                return Response({'error': 'Invalid start_date format. Use YYYY-MM-DD'},
                                status=status.HTTP_400_BAD_REQUEST)

        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                logger.error(f"Invalid start_date format: {end_date}")
                return Response({'error': 'Invalid end_date format. Use YYYY-MM-DD'},
                                status=status.HTTP_400_BAD_REQUEST)

        winners = self.winner_use_cases.get_winners_by_date_range(start_date_obj, end_date_obj)
        serializer = DailyWinnerSerializer(winners, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's winner"""
        # today = timezone.now().date()
        winner = self.winner_use_cases.get_daily_winner()

        if winner:
            serializer = DailyWinnerSerializer(winner)
            return Response(serializer.data)
        logger.info("No votes recorded for today yet")
        return Response({'message': 'No votes recorded for today yet'},
                        status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Manually trigger winner calculation for a specific date"""
        date_str = request.data.get('date')

        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                logger.error(f"Invalid date format: {date_str}")
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            target_date = timezone.now().date()

        winner = self.winner_use_cases.force_calculate_winner(target_date)

        if winner:
            serializer = DailyWinnerSerializer(winner)
            return Response(serializer.data)
        logger.info(f"No votes recorded for {target_date}")
        return Response({'message': f'No votes recorded for {target_date}'},
                        status=status.HTTP_404_NOT_FOUND)