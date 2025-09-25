"""
خدمة الأخبار - مشروع نائبك
Flask + SQLite News Service
"""
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from datetime import datetime, timedelta
import os
import logging
from functools import wraps
import sqlite3

# إعداد التطبيق
app = Flask(__name__)

# تحميل التكوين
if os.path.exists('config_updated.py'):
    from config_updated import current_config
    app.config.from_object(current_config)
else:
    # إعدادات افتراضية
    app.config['SECRET_KEY'] = 'naebak-news-service-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///naebak_news.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إعداد المكونات
db = SQLAlchemy(app)
cors = CORS(app)
cache = Cache(app)
mail = Mail(app)

# إعداد Rate Limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# استيراد النماذج
try:
    from app.models import (
        NewsCategory, NewsTag, NewsItem, NewsComment, 
        NewsStats, NewsSettings
    )
except ImportError:
    logger.warning("لم يتم العثور على نماذج البيانات")


def require_api_key(f):
    """التحقق من مفتاح API"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != app.config.get('API_KEY'):
            return jsonify({'error': 'مفتاح API غير صحيح'}), 401
        return f(*args, **kwargs)
    return decorated_function


def require_admin_key(f):
    """التحقق من مفتاح الإدارة"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_key = request.headers.get('X-Admin-Key')
        if not admin_key or admin_key != app.config.get('ADMIN_KEY'):
            return jsonify({'error': 'مفتاح الإدارة غير صحيح'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    """إعداد قبل كل طلب"""
    g.start_time = datetime.utcnow()


@app.after_request
def after_request(response):
    """إعداد بعد كل طلب"""
    # إضافة headers للأمان
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # إضافة وقت الاستجابة
    if hasattr(g, 'start_time'):
        response_time = (datetime.utcnow() - g.start_time).total_seconds()
        response.headers['X-Response-Time'] = f'{response_time:.3f}s'
    
    return response


@app.route('/health', methods=['GET'])
def health_check():
    """فحص صحة الخدمة"""
    try:
        # فحص قاعدة البيانات
        db.session.execute('SELECT 1')
        
        # فحص Redis (إذا كان متاحاً)
        cache_status = 'متاح'
        try:
            cache.get('test')
        except:
            cache_status = 'غير متاح'
        
        return jsonify({
            'status': 'healthy',
            'service': app.config.get('SERVICE_NAME', 'naebak-news-service'),
            'version': app.config.get('SERVICE_VERSION', '1.0.0'),
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'متصل',
            'cache': cache_status,
            'uptime': 'متاح'
        })
    except Exception as e:
        logger.error(f"خطأ في فحص الصحة: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/api/news', methods=['GET'])
@limiter.limit("50 per minute")
def get_news():
    """الحصول على قائمة الأخبار"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        category = request.args.get('category')
        tag = request.args.get('tag')
        featured = request.args.get('featured', type=bool)
        breaking = request.args.get('breaking', type=bool)
        
        # بناء الاستعلام
        query = NewsItem.query.filter_by(is_published=True)
        
        if category:
            query = query.join(NewsCategory).filter(NewsCategory.name == category)
        
        if tag:
            query = query.join(NewsItem.tags).filter(NewsTag.name == tag)
        
        if featured is not None:
            query = query.filter(NewsItem.is_featured == featured)
            
        if breaking is not None:
            query = query.filter(NewsItem.is_breaking == breaking)
        
        # ترتيب حسب الأولوية والتاريخ
        query = query.order_by(NewsItem.priority.desc(), NewsItem.published_at.desc())
        
        # تطبيق التصفح
        news_items = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'news': [{
                'id': item.id,
                'title': item.title,
                'slug': item.slug,
                'summary': item.summary,
                'category': item.category.name if item.category else None,
                'tags': [tag.name for tag in item.tags],
                'is_featured': item.is_featured,
                'is_breaking': item.is_breaking,
                'priority': item.priority,
                'author_name': item.author_name,
                'published_at': item.published_at.isoformat() if item.published_at else None,
                'view_count': item.view_count,
                'like_count': item.like_count,
                'comment_count': item.comment_count
            } for item in news_items.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': news_items.total,
                'pages': news_items.pages,
                'has_next': news_items.has_next,
                'has_prev': news_items.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على الأخبار: {str(e)}")
        return jsonify({'error': 'خطأ في الخادم'}), 500


@app.route('/api/news/<slug>', methods=['GET'])
@limiter.limit("30 per minute")
def get_news_item(slug):
    """الحصول على خبر محدد"""
    try:
        news_item = NewsItem.query.filter_by(slug=slug, is_published=True).first()
        if not news_item:
            return jsonify({'error': 'الخبر غير موجود'}), 404
        
        # تحديث عدد المشاهدات
        news_item.view_count += 1
        db.session.commit()
        
        return jsonify({
            'id': news_item.id,
            'title': news_item.title,
            'slug': news_item.slug,
            'summary': news_item.summary,
            'content': news_item.content,
            'category': {
                'name': news_item.category.name,
                'color': news_item.category.color
            } if news_item.category else None,
            'tags': [{
                'name': tag.name,
                'color': tag.color
            } for tag in news_item.tags],
            'is_featured': news_item.is_featured,
            'is_breaking': news_item.is_breaking,
            'priority': news_item.priority,
            'author_name': news_item.author_name,
            'published_at': news_item.published_at.isoformat() if news_item.published_at else None,
            'updated_at': news_item.updated_at.isoformat() if news_item.updated_at else None,
            'view_count': news_item.view_count,
            'like_count': news_item.like_count,
            'share_count': news_item.share_count,
            'comment_count': news_item.comment_count,
            'meta_title': news_item.meta_title,
            'meta_description': news_item.meta_description
        })
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على الخبر: {str(e)}")
        return jsonify({'error': 'خطأ في الخادم'}), 500


@app.route('/api/categories', methods=['GET'])
@cache.cached(timeout=300)
def get_categories():
    """الحصول على تصنيفات الأخبار"""
    try:
        categories = NewsCategory.query.filter_by(is_active=True).order_by(NewsCategory.display_order).all()
        
        return jsonify({
            'categories': [{
                'id': cat.id,
                'name': cat.name,
                'name_en': cat.name_en,
                'description': cat.description,
                'icon': cat.icon,
                'color': cat.color,
                'news_count': cat.news_count
            } for cat in categories]
        })
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على التصنيفات: {str(e)}")
        return jsonify({'error': 'خطأ في الخادم'}), 500


@app.route('/api/tags', methods=['GET'])
@cache.cached(timeout=300)
def get_tags():
    """الحصول على علامات الأخبار"""
    try:
        tags = NewsTag.query.filter_by(is_active=True).order_by(NewsTag.usage_count.desc()).limit(20).all()
        
        return jsonify({
            'tags': [{
                'id': tag.id,
                'name': tag.name,
                'name_en': tag.name_en,
                'color': tag.color,
                'usage_count': tag.usage_count
            } for tag in tags]
        })
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على العلامات: {str(e)}")
        return jsonify({'error': 'خطأ في الخادم'}), 500


@app.route('/api/stats', methods=['GET'])
@require_api_key
def get_stats():
    """الحصول على إحصائيات الخدمة"""
    try:
        total_news = NewsItem.query.filter_by(is_published=True).count()
        total_categories = NewsCategory.query.filter_by(is_active=True).count()
        total_tags = NewsTag.query.filter_by(is_active=True).count()
        total_comments = NewsComment.query.filter_by(is_approved=True).count()
        
        # إحصائيات اليوم
        today = datetime.utcnow().date()
        today_stats = NewsStats.query.filter_by(date=today).first()
        
        return jsonify({
            'total_news': total_news,
            'total_categories': total_categories,
            'total_tags': total_tags,
            'total_comments': total_comments,
            'today_views': today_stats.views if today_stats else 0,
            'today_likes': today_stats.likes if today_stats else 0,
            'today_shares': today_stats.shares if today_stats else 0
        })
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على الإحصائيات: {str(e)}")
        return jsonify({'error': 'خطأ في الخادم'}), 500


@app.route('/api/admin/load-data', methods=['POST'])
@require_admin_key
def load_initial_data():
    """تحميل البيانات الأساسية"""
    try:
        from app.utils.load_data import load_all_initial_data
        
        success = load_all_initial_data()
        if success:
            return jsonify({'message': 'تم تحميل البيانات الأساسية بنجاح'})
        else:
            return jsonify({'error': 'فشل في تحميل البيانات'}), 500
            
    except Exception as e:
        logger.error(f"خطأ في تحميل البيانات: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """معالج خطأ 404"""
    return jsonify({'error': 'المورد غير موجود'}), 404


@app.errorhandler(500)
def internal_error(error):
    """معالج خطأ 500"""
    logger.error(f"خطأ داخلي: {str(error)}")
    return jsonify({'error': 'خطأ داخلي في الخادم'}), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    """معالج تجاوز الحد المسموح"""
    return jsonify({'error': 'تم تجاوز الحد المسموح من الطلبات'}), 429


def create_tables():
    """إنشاء جداول قاعدة البيانات"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("تم إنشاء جداول قاعدة البيانات بنجاح")
    except Exception as e:
        logger.error(f"خطأ في إنشاء الجداول: {str(e)}")


if __name__ == '__main__':
    # إنشاء الجداول
    create_tables()
    
    # تشغيل التطبيق
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 8009)
    debug = app.config.get('DEBUG', False)
    
    logger.info(f"🚀 بدء تشغيل خدمة الأخبار على {host}:{port}")
    logger.info(f"📊 وضع التطوير: {'مفعل' if debug else 'معطل'}")
    logger.info(f"🗄️ قاعدة البيانات: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    app.run(host=host, port=port, debug=debug)
