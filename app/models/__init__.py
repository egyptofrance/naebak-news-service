"""
نماذج خدمة الأخبار - مشروع نائبك
"""
from .models import (
    db,
    NewsCategory,
    NewsTag,
    NewsItem,
    NewsComment,
    NewsStats,
    NewsSettings,
    news_tags_association
)

__all__ = [
    'db',
    'NewsCategory',
    'NewsTag', 
    'NewsItem',
    'NewsComment',
    'NewsStats',
    'NewsSettings',
    'news_tags_association'
]
