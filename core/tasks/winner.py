from celery import shared_task
from django.utils import timezone
from core.services.winner_calculation import WinnerCalculationService
import logging

logger = logging.getLogger(__name__)

@shared_task
def run_daily_winner_calculation():
    from infrastructure.repositories.django_vote import DjangoVoteRepository
    logger.info("Running daily winner calculation task...")
    today = timezone.now().date()
    try:
        service = WinnerCalculationService(DjangoVoteRepository())
        result = service.calculate_daily_winner()
        if result:
            logger.info(f"Winner for {today}: {result.restaurant_name} ({result.total_score} points)")
        else:
            logger.info(f"No winner could be determined for {today}")
    except Exception as e:
        logger.error(f"Error during winner calculation: {e}")
        raise e