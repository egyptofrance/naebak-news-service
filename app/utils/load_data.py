"""
أداة تحميل البيانات الأساسية لخدمة الأخبار - مشروع نائبك
"""
from app.models import (
    db, NewsCategory, NewsTag, NewsItem, NewsComment, 
    NewsStats, NewsSettings
)
from app.data.initial_data import (
    NEWS_CATEGORIES, NEWS_TAGS, SAMPLE_NEWS, SAMPLE_COMMENTS,
    NEWS_SETTINGS, SAMPLE_STATS
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def load_news_categories():
    """تحميل تصنيفات الأخبار"""
    try:
        logger.info("بدء تحميل تصنيفات الأخبار...")
        
        for category_data in NEWS_CATEGORIES:
            # التحقق من وجود التصنيف
            existing = NewsCategory.query.filter_by(name=category_data['name']).first()
            if not existing:
                category = NewsCategory(
                    name=category_data['name'],
                    name_en=category_data['name_en'],
                    description=category_data['description'],
                    description_en=category_data['description_en'],
                    icon=category_data['icon'],
                    color=category_data['color'],
                    display_order=category_data['display_order']
                )
                db.session.add(category)
                logger.info(f"تم إضافة تصنيف: {category.name}")
        
        db.session.commit()
        logger.info(f"تم تحميل {len(NEWS_CATEGORIES)} تصنيف أخبار بنجاح")
        
    except Exception as e:
        logger.error(f"خطأ في تحميل تصنيفات الأخبار: {str(e)}")
        db.session.rollback()
        raise


def load_news_tags():
    """تحميل علامات الأخبار"""
    try:
        logger.info("بدء تحميل علامات الأخبار...")
        
        for tag_data in NEWS_TAGS:
            # التحقق من وجود العلامة
            existing = NewsTag.query.filter_by(name=tag_data['name']).first()
            if not existing:
                tag = NewsTag(
                    name=tag_data['name'],
                    name_en=tag_data['name_en'],
                    description=tag_data['description'],
                    color=tag_data['color']
                )
                db.session.add(tag)
                logger.info(f"تم إضافة علامة: {tag.name}")
        
        db.session.commit()
        logger.info(f"تم تحميل {len(NEWS_TAGS)} علامة أخبار بنجاح")
        
    except Exception as e:
        logger.error(f"خطأ في تحميل علامات الأخبار: {str(e)}")
        db.session.rollback()
        raise


def load_sample_news():
    """تحميل الأخبار التجريبية"""
    try:
        logger.info("بدء تحميل الأخبار التجريبية...")
        
        for news_data in SAMPLE_NEWS:
            # التحقق من وجود الخبر
            existing = NewsItem.query.filter_by(slug=news_data['slug']).first()
            if not existing:
                # البحث عن التصنيف
                category = NewsCategory.query.filter_by(name=news_data['category_name']).first()
                if not category:
                    logger.warning(f"لم يتم العثور على التصنيف: {news_data['category_name']}")
                    continue
                
                # إنشاء الخبر
                news_item = NewsItem(
                    title=news_data['title'],
                    title_en=news_data.get('title_en'),
                    slug=news_data['slug'],
                    summary=news_data['summary'],
                    summary_en=news_data.get('summary_en'),
                    content=news_data['content'],
                    category_id=category.id,
                    status='published' if news_data['is_published'] else 'draft',
                    is_published=news_data['is_published'],
                    is_featured=news_data.get('is_featured', False),
                    is_breaking=news_data.get('is_breaking', False),
                    priority=news_data.get('priority', 0),
                    author_name=news_data.get('author_name'),
                    view_count=news_data.get('view_count', 0),
                    like_count=news_data.get('like_count', 0),
                    share_count=news_data.get('share_count', 0),
                    published_at=news_data.get('published_at'),
                    meta_title=news_data['title'],
                    meta_description=news_data['summary']
                )
                
                db.session.add(news_item)
                db.session.flush()  # للحصول على ID
                
                # إضافة العلامات
                if 'tags' in news_data:
                    for tag_name in news_data['tags']:
                        tag = NewsTag.query.filter_by(name=tag_name).first()
                        if tag:
                            news_item.tags.append(tag)
                            tag.usage_count += 1
                
                logger.info(f"تم إضافة خبر: {news_item.title}")
        
        db.session.commit()
        logger.info(f"تم تحميل {len(SAMPLE_NEWS)} خبر تجريبي بنجاح")
        
    except Exception as e:
        logger.error(f"خطأ في تحميل الأخبار التجريبية: {str(e)}")
        db.session.rollback()
        raise


def load_sample_comments():
    """تحميل التعليقات التجريبية"""
    try:
        logger.info("بدء تحميل التعليقات التجريبية...")
        
        for comment_data in SAMPLE_COMMENTS:
            # البحث عن الخبر
            news_item = NewsItem.query.filter_by(slug=comment_data['news_slug']).first()
            if not news_item:
                logger.warning(f"لم يتم العثور على الخبر: {comment_data['news_slug']}")
                continue
            
            # التحقق من وجود التعليق
            existing = NewsComment.query.filter_by(
                news_item_id=news_item.id,
                user_email=comment_data['user_email'],
                content=comment_data['content']
            ).first()
            
            if not existing:
                comment = NewsComment(
                    news_item_id=news_item.id,
                    user_name=comment_data['user_name'],
                    user_email=comment_data['user_email'],
                    content=comment_data['content'],
                    is_approved=comment_data.get('is_approved', False),
                    approved_at=datetime.utcnow() if comment_data.get('is_approved') else None
                )
                
                db.session.add(comment)
                
                # تحديث عدد التعليقات في الخبر
                if comment.is_approved:
                    news_item.comment_count += 1
                
                logger.info(f"تم إضافة تعليق من: {comment.user_name}")
        
        db.session.commit()
        logger.info(f"تم تحميل {len(SAMPLE_COMMENTS)} تعليق تجريبي بنجاح")
        
    except Exception as e:
        logger.error(f"خطأ في تحميل التعليقات التجريبية: {str(e)}")
        db.session.rollback()
        raise


def load_news_settings():
    """تحميل إعدادات النظام"""
    try:
        logger.info("بدء تحميل إعدادات النظام...")
        
        for setting_data in NEWS_SETTINGS:
            # التحقق من وجود الإعداد
            existing = NewsSettings.query.filter_by(setting_key=setting_data['setting_key']).first()
            if not existing:
                setting = NewsSettings(
                    setting_key=setting_data['setting_key'],
                    setting_value=setting_data['setting_value'],
                    setting_type=setting_data['setting_type'],
                    description=setting_data['description'],
                    category=setting_data['category'],
                    is_public=setting_data.get('is_public', False)
                )
                db.session.add(setting)
                logger.info(f"تم إضافة إعداد: {setting.setting_key}")
        
        db.session.commit()
        logger.info(f"تم تحميل {len(NEWS_SETTINGS)} إعداد نظام بنجاح")
        
    except Exception as e:
        logger.error(f"خطأ في تحميل إعدادات النظام: {str(e)}")
        db.session.rollback()
        raise


def load_sample_stats():
    """تحميل الإحصائيات التجريبية"""
    try:
        logger.info("بدء تحميل الإحصائيات التجريبية...")
        
        for stat_data in SAMPLE_STATS:
            # التحقق من وجود الإحصائية
            existing = NewsStats.query.filter_by(
                news_item_id=stat_data['news_item_id'],
                date=stat_data['date']
            ).first()
            
            if not existing:
                stat = NewsStats(
                    news_item_id=stat_data['news_item_id'],
                    date=stat_data['date'],
                    views=stat_data['views'],
                    unique_views=stat_data['unique_views'],
                    likes=stat_data['likes'],
                    shares=stat_data['shares'],
                    comments=stat_data['comments'],
                    avg_read_time=stat_data['avg_read_time'],
                    bounce_rate=stat_data['bounce_rate'],
                    engagement_rate=stat_data['engagement_rate'],
                    direct_visits=stat_data['direct_visits'],
                    social_visits=stat_data['social_visits'],
                    search_visits=stat_data['search_visits'],
                    referral_visits=stat_data['referral_visits']
                )
                db.session.add(stat)
        
        db.session.commit()
        logger.info(f"تم تحميل {len(SAMPLE_STATS)} إحصائية تجريبية بنجاح")
        
    except Exception as e:
        logger.error(f"خطأ في تحميل الإحصائيات التجريبية: {str(e)}")
        db.session.rollback()
        raise


def load_all_initial_data():
    """تحميل جميع البيانات الأساسية"""
    try:
        logger.info("بدء تحميل جميع البيانات الأساسية لخدمة الأخبار...")
        
        # تحميل البيانات بالترتيب الصحيح
        load_news_categories()
        load_news_tags()
        load_sample_news()
        load_sample_comments()
        load_news_settings()
        load_sample_stats()
        
        logger.info("تم تحميل جميع البيانات الأساسية بنجاح! ✅")
        
        # طباعة ملخص
        categories_count = NewsCategory.query.count()
        tags_count = NewsTag.query.count()
        news_count = NewsItem.query.count()
        comments_count = NewsComment.query.count()
        settings_count = NewsSettings.query.count()
        stats_count = NewsStats.query.count()
        
        logger.info(f"""
📊 ملخص البيانات المحملة:
- التصنيفات: {categories_count}
- العلامات: {tags_count}
- الأخبار: {news_count}
- التعليقات: {comments_count}
- الإعدادات: {settings_count}
- الإحصائيات: {stats_count}
        """)
        
        return True
        
    except Exception as e:
        logger.error(f"خطأ في تحميل البيانات الأساسية: {str(e)}")
        return False


if __name__ == '__main__':
    # تشغيل تحميل البيانات
    load_all_initial_data()
