'''
Naebak News Service - Flask Application

This is the main application file for the Naebak News Service. It defines the Flask application, configures extensions, and sets up the API endpoints.

The service provides endpoints for retrieving news articles, categories, and tags, as well as for service health checks and administrative tasks.
'''
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

# App setup
app = Flask(__name__)

# Load configuration
if os.path.exists('config_updated.py'):
    from config_updated import current_config
    app.config.from_object(current_config)
else:
    # Default settings
    app.config['SECRET_KEY'] = 'naebak-news-service-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///naebak_news.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup components
db = SQLAlchemy(app)
cors = CORS(app)
cache = Cache(app)
mail = Mail(app)

# Setup Rate Limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import models
try:
    from app.models import (
        NewsCategory, NewsTag, NewsItem, NewsComment, 
        NewsStats, NewsSettings
    )
except ImportError:
    logger.warning("Data models not found")

def require_api_key(f):
    '''Decorator to require an API key for an endpoint.'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != app.config.get('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_admin_key(f):
    '''Decorator to require an admin key for an endpoint.'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_key = request.headers.get('X-Admin-Key')
        if not admin_key or admin_key != app.config.get('ADMIN_KEY'):
            return jsonify({'error': 'Invalid admin key'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    '''Set up before each request.'''
    g.start_time = datetime.utcnow()


@app.after_request
def after_request(response):
    '''Set up after each request.'''
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Add response time
    if hasattr(g, 'start_time'):
        response_time = (datetime.utcnow() - g.start_time).total_seconds()
        response.headers['X-Response-Time'] = f'{response_time:.3f}s'
    
    return response


@app.route('/health', methods=['GET'])
def health_check():
    '''
    Health check endpoint for the service.

    This endpoint is used to monitor the health of the service. It checks the
    database connection and the cache status.

    Returns:
        A JSON response with the health status of the service.
    '''
    try:
        # Check database
        db.session.execute('SELECT 1')
        
        # Check Redis (if available)
        cache_status = 'available'
        try:
            cache.get('test')
        except:
            cache_status = 'unavailable'
        
        return jsonify({
            'status': 'healthy',
            'service': app.config.get('SERVICE_NAME', 'naebak-news-service'),
            'version': app.config.get('SERVICE_VERSION', '1.0.0'),
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected',
            'cache': cache_status,
            'uptime': 'available'
        })
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/api/news', methods=['GET'])
@limiter.limit("50 per minute")
def get_news():
    '''
    Get a list of news items.

    This endpoint returns a paginated list of published news items. The list can be
    filtered by category, tag, featured status, and breaking news status.

    Args (query parameters):
        page (int): The page number for pagination.
        per_page (int): The number of items per page.
        category (str): The name of the category to filter by.
        tag (str): The name of the tag to filter by.
        featured (bool): Whether to filter by featured status.
        breaking (bool): Whether to filter by breaking news status.

    Returns:
        A JSON response with a list of news items and pagination information.
    '''
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        category = request.args.get('category')
        tag = request.args.get('tag')
        featured = request.args.get('featured', type=bool)
        breaking = request.args.get('breaking', type=bool)
        
        # Build query
        query = NewsItem.query.filter_by(is_published=True)
        
        if category:
            query = query.join(NewsCategory).filter(NewsCategory.name == category)
        
        if tag:
            query = query.join(NewsItem.tags).filter(NewsTag.name == tag)
        
        if featured is not None:
            query = query.filter(NewsItem.is_featured == featured)
            
        if breaking is not None:
            query = query.filter(NewsItem.is_breaking == breaking)
        
        # Order by priority and date
        query = query.order_by(NewsItem.priority.desc(), NewsItem.published_at.desc())
        
        # Apply pagination
        news_items = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'news': [item.to_dict() for item in news_items.items],
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
        logger.error(f"Error getting news: {str(e)}")
        return jsonify({'error': 'Server error'}), 500


@app.route('/api/news/<slug>', methods=['GET'])
@limiter.limit("30 per minute")
def get_news_item(slug):
    '''
    Get a specific news item.

    This endpoint returns the details of a specific news item, identified by its slug.
    It also increments the view count for the news item.

    Args:
        slug (str): The slug of the news item.

    Returns:
        A JSON response with the details of the news item.
    '''
    try:
        news_item = NewsItem.query.filter_by(slug=slug, is_published=True).first()
        if not news_item:
            return jsonify({'error': 'News item not found'}), 404
        
        # Update view count
        news_item.increment_view_count()
        
        return jsonify(news_item.to_dict(include_content=True))
        
    except Exception as e:
        logger.error(f"Error getting news item: {str(e)}")
        return jsonify({'error': 'Server error'}), 500


@app.route('/api/categories', methods=['GET'])
@cache.cached(timeout=300)
def get_categories():
    '''
    Get a list of news categories.

    This endpoint returns a list of all active news categories, ordered by display order.

    Returns:
        A JSON response with a list of news categories.
    '''
    try:
        categories = NewsCategory.query.filter_by(is_active=True).order_by(NewsCategory.display_order).all()
        
        return jsonify({'categories': [cat.to_dict() for cat in categories]})
        
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        return jsonify({'error': 'Server error'}), 500


@app.route('/api/tags', methods=['GET'])
@cache.cached(timeout=300)
def get_tags():
    '''
    Get a list of news tags.

    This endpoint returns a list of the top 20 most used active news tags.

    Returns:
        A JSON response with a list of news tags.
    '''
    try:
        tags = NewsTag.query.filter_by(is_active=True).order_by(NewsTag.usage_count.desc()).limit(20).all()
        
        return jsonify({'tags': [tag.to_dict() for tag in tags]})
        
    except Exception as e:
        logger.error(f"Error getting tags: {str(e)}")
        return jsonify({'error': 'Server error'}), 500


@app.route('/api/stats', methods=['GET'])
@require_api_key
def get_stats():
    '''
    Get service statistics.

    This endpoint returns statistics about the news service, including the total
    number of news items, categories, tags, and comments.

    Returns:
        A JSON response with the service statistics.
    '''
    try:
        total_news = NewsItem.query.filter_by(is_published=True).count()
        total_categories = NewsCategory.query.filter_by(is_active=True).count()
        total_tags = NewsTag.query.filter_by(is_active=True).count()
        total_comments = NewsComment.query.filter_by(is_approved=True).count()
        
        # Today's stats
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
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Server error'}), 500


@app.route('/api/admin/load-data', methods=['POST'])
@require_admin_key
def load_initial_data():
    '''
    Load initial data.

    This is an admin-only endpoint for loading initial data into the database.

    Returns:
        A JSON response with a success or error message.
    '''
    try:
        from app.utils.load_data import load_all_initial_data
        
        success = load_all_initial_data()
        if success:
            return jsonify({'message': 'Initial data loaded successfully'})
        else:
            return jsonify({'error': 'Failed to load data'}), 500
            
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    '''404 error handler.'''
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    '''500 error handler.'''
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    '''Ratelimit error handler.'''
    return jsonify({'error': 'Ratelimit exceeded'}), 429

def create_tables():
    '''Create database tables.'''
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")


if __name__ == '__main__':
    # Create tables
    create_tables()
    
    # Run app
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 8009)
    debug = app.config.get('DEBUG', False)
    
    logger.info(f"🚀 Starting news service on {host}:{port}")
    logger.info(f"📊 Debug mode: {'enabled' if debug else 'disabled'}")
    logger.info(f"🗄️ Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    app.run(host=host, port=port, debug=debug)
'''
