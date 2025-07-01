from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from core.use_cases.voting_use_cases import VotingUseCases
from core.use_cases.winner_use_cases import WinnerUseCases
from infrastructure.repositories.django_restaurant import DjangoRestaurantRepository
from infrastructure.repositories.django_vote import DjangoVoteRepository
from infrastructure.repositories.django_winner import DjangoWinnerRepository
import logging
from .serializers import (
    VoteCreateSerializer,
    UserVoteStatsSerializer
)

logger = logging.getLogger(__name__)

class VoteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vote_repo = DjangoVoteRepository()
        self.restaurant_repo = DjangoRestaurantRepository()
        self.winner_repo = DjangoWinnerRepository()
        self.voting_use_cases = VotingUseCases(self.vote_repo, self.restaurant_repo)
        self.winner_use_cases = WinnerUseCases(self.vote_repo, self.restaurant_repo, self.winner_repo)

    def list(self, request):
        """Get user's votes for today"""
        today = timezone.now().date()
        votes = self.voting_use_cases.get_user_votes(request.user.id, today)

        # Convert to serializable format
        votes_data = []
        for vote in votes:
            votes_data.append({
                'id': vote.id,
                'user_id': vote.user_id,
                'restaurant_id': vote.restaurant_id,
                'weight': float(vote.weight),
                'created_at': vote.created_at
            })

        return Response(votes_data)

    def create(self, request):
        """Create a single vote"""
        serializer = VoteCreateSerializer(data=request.data)
        if serializer.is_valid():
            today = timezone.now()
            if timezone.localtime(today).hour >= 12:
                logger.error(f"Voting is closed for today: {today}")
                return Response({'error': 'Voting is closed for today'}, status=status.HTTP_400_BAD_REQUEST)
            vote_day = today.date()

            vote, error_msg = self.voting_use_cases.create_vote(
                restaurant_id=serializer.validated_data['restaurant_id'],
                user_id=request.user.id,
                vote_date=vote_day
            )

            if vote:
                vote_data = {
                    'id': vote.id,
                    'user_id': vote.user_id,
                    'restaurant_id': vote.restaurant_id,
                    'weight': float(vote.weight),
                    'created_at': vote.created_at
                }
                logger.info(f"User {request.user.username} voted for restaurant {vote.restaurant_id} with weight {vote.weight} on {vote_day}")
                return Response(vote_data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"User {request.user.username} failed to vote: {error_msg}")
                return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)