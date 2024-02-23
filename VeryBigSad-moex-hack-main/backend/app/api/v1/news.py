import logging

from fastapi import APIRouter, status
from tortoise.exceptions import DoesNotExist

from core.exceptions import DatabaseInternalError, ArticleNotFound
from core.models import News
from core.schemas.news import NewsResponse, DetailedNewsResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[NewsResponse]
)
async def get_news():
    """List of news articles"""
    try:
        return await News.filter(is_active=True)
    except Exception as e:
        logger.exception(e)
        raise DatabaseInternalError()


@router.get(
    "/{news_id}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedNewsResponse
)
async def get_news_by_id(news_id: int):
    """Get news article by id"""
    try:
        return await News.filter(is_active=True).get(id=news_id)
    except DoesNotExist:
        raise ArticleNotFound()
    except Exception as e:
        logger.exception(e)
        raise DatabaseInternalError()
