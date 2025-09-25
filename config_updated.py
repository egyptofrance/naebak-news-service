"""
إعدادات خدمة الأخبار - مشروع نائبك
Flask + SQLite Configuration
"""
import os
from datetime import timedelta


class Config:
    """إعدادات التطبيق الأساسية"""
    
    # إعدادات التطبيق
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'naebak-news-service-secret-key-2024'
    
    # إعدادات قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///naebak_news.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # إعدادات Redis للتخزين المؤقت
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    REDIS_DB = int(os.environ.get('REDIS_DB') or 3)
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    
    # إعدادات التخزين المؤقت
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = REDIS_HOST
    CACHE_REDIS_PORT = REDIS_PORT
    CACHE_REDIS_DB = REDIS_DB
    CACHE_REDIS_PASSWORD = REDIS_PASSWORD
    CACHE_DEFAULT_TIMEOUT = 300  # 5 دقائق
    
    # إعدادات الخدمة
    SERVICE_NAME = 'naebak-news-service'
    SERVICE_VERSION = '1.0.0'
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 8009)
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # إعدادات الأمان
    API_KEY = os.environ.get('API_KEY') or 'naebak-news-api-key-2024'
    ADMIN_KEY = os.environ.get('ADMIN_KEY') or 'naebak-news-admin-key-2024'
    
    # إعدادات CORS
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:3001', 
        'https://naebak.com',
        'https://www.naebak.com',
        'https://admin.naebak.com'
    ]
    
    # إعدادات رفع الملفات
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx'}
    
    # إعدادات الصور
    IMAGE_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'images')
    THUMBNAIL_SIZE = (300, 200)
    LARGE_IMAGE_SIZE = (1200, 800)
    
    # إعدادات المحتوى
    MAX_TITLE_LENGTH = 200
    MAX_SUMMARY_LENGTH = 500
    MAX_CONTENT_LENGTH = 50000
    MAX_COMMENT_LENGTH = 500
    
    # إعدادات الصفحات
    NEWS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 20
    FEATURED_NEWS_COUNT = 5
    BREAKING_NEWS_DURATION = 24  # ساعة
    
    # إعدادات SEO
    DEFAULT_META_TITLE = 'نائبك - أخبار'
    DEFAULT_META_DESCRIPTION = 'آخر الأخبار والتطورات من منصة نائبك'
    DEFAULT_META_KEYWORDS = 'نائبك، أخبار، مصر، برلمان، نواب، سياسة'
    
    # إعدادات التعليقات
    COMMENTS_ENABLED = True
    COMMENTS_MODERATION = True
    COMMENTS_PER_NEWS = 100
    
    # إعدادات الإحصائيات
    STATS_RETENTION_DAYS = 365
    STATS_UPDATE_INTERVAL = 3600  # ساعة
    
    # إعدادات التنظيف التلقائي
    AUTO_CLEANUP_ENABLED = True
    CLEANUP_INTERVAL = 86400  # يوم
    OLD_STATS_CLEANUP_DAYS = 365
    OLD_COMMENTS_CLEANUP_DAYS = 180
    
    # إعدادات البحث
    SEARCH_RESULTS_PER_PAGE = 15
    SEARCH_MIN_LENGTH = 3
    SEARCH_MAX_LENGTH = 100
    
    # إعدادات الأرشفة
    AUTO_ARCHIVE_ENABLED = True
    AUTO_ARCHIVE_DAYS = 365
    
    # إعدادات الإشعارات
    NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL') or 'http://localhost:8007'
    
    # إعدادات التكامل مع الخدمات الأخرى
    AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL') or 'http://localhost:8001'
    ADMIN_SERVICE_URL = os.environ.get('ADMIN_SERVICE_URL') or 'http://localhost:8006'
    
    # إعدادات المراقبة
    MONITORING_ENABLED = True
    HEALTH_CHECK_INTERVAL = 60
    METRICS_RETENTION_HOURS = 24
    
    # إعدادات الأداء
    ENABLE_GZIP = True
    ENABLE_ETAG = True
    CACHE_STATIC_FILES = True
    
    # إعدادات الأمان المتقدمة
    RATE_LIMIT_STORAGE_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    RATE_LIMIT_DEFAULT = '100 per hour'
    RATE_LIMIT_NEWS_CREATE = '10 per hour'
    RATE_LIMIT_COMMENT_CREATE = '20 per hour'
    
    # إعدادات التوقيت
    TIMEZONE = 'Africa/Cairo'
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # إعدادات اللغة
    DEFAULT_LANGUAGE = 'ar'
    SUPPORTED_LANGUAGES = ['ar', 'en']
    
    # إعدادات وسائل التواصل الاجتماعي
    SOCIAL_SHARING_ENABLED = True
    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    TWITTER_HANDLE = os.environ.get('TWITTER_HANDLE') or '@naebak_egypt'
    
    # إعدادات البريد الإلكتروني
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'news@naebak.com'


class DevelopmentConfig(Config):
    """إعدادات بيئة التطوير"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///naebak_news_dev.db'
    CACHE_TYPE = 'simple'
    RATE_LIMIT_DEFAULT = '1000 per hour'


class ProductionConfig(Config):
    """إعدادات بيئة الإنتاج"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///naebak_news_prod.db'
    
    # إعدادات أمان الإنتاج
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # إعدادات SSL
    PREFERRED_URL_SCHEME = 'https'
    
    # إعدادات الأداء
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=12)


class TestingConfig(Config):
    """إعدادات بيئة الاختبار"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
    RATE_LIMIT_ENABLED = False


# اختيار التكوين حسب البيئة
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# الحصول على التكوين الحالي
current_config = config.get(os.environ.get('FLASK_ENV', 'default'), DevelopmentConfig)
