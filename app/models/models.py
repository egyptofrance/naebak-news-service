'''
News Service Models - Naebak Project
Flask + SQLAlchemy Models

This module defines the database models for the Naebak News Service.
It includes models for news categories, tags, news items, comments, statistics, and settings.
'''
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()


class NewsCategory(db.Model):
    """Represents a category for news items.

    Attributes:
        id (int): The primary key.
        name (str): The name of the category in Arabic.
        name_en (str): The name of the category in English.
        description (str): A description of the category in Arabic.
        description_en (str): A description of the category in English.
        icon (str): An icon for the category (e.g., FontAwesome class).
        color (str): A hex color code for the category.
        display_order (int): The order in which the category should be displayed.
        is_active (bool): Whether the category is active and should be displayed.
        created_at (datetime): The timestamp when the category was created.
        news_items (relationship): A relationship to the news items in this category.
    """
    __tablename__ = 'news_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    name_en = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(7), default='#007BFF')
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    news_items = db.relationship('NewsItem', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<NewsCategory {self.name}>'

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'description': self.description,
            'description_en': self.description_en,
            'icon': self.icon,
            'color': self.color,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'news_count': self.news_items.filter_by(is_published=True).count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class NewsTag(db.Model):
    """Represents a tag for news items.

    Attributes:
        id (int): The primary key.
        name (str): The name of the tag in Arabic.
        name_en (str): The name of the tag in English.
        description (str): A description of the tag.
        color (str): A hex color code for the tag.
        usage_count (int): The number of times the tag has been used.
        is_active (bool): Whether the tag is active.
        created_at (datetime): The timestamp when the tag was created.
    """
    __tablename__ = 'news_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    name_en = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#6C757D')
    usage_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NewsTag {self.name}>'

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'description': self.description,
            'color': self.color,
            'usage_count': self.usage_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Association table for NewsItem and NewsTag
news_tags_association = db.Table('news_item_tags',
    db.Column('news_item_id', db.Integer, db.ForeignKey('news_items.id'), primary_key=True),
    db.Column('news_tag_id', db.Integer, db.ForeignKey('news_tags.id'), primary_key=True)
)


class NewsItem(db.Model):
    """Represents a news item or article.

    Attributes:
        id (int): The primary key.
        title (str): The title of the news item.
        title_en (str): The English title of the news item.
        slug (str): The URL-friendly slug for the news item.
        summary (str): A short summary of the news item.
        summary_en (str): The English summary of the news item.
        content (str): The full content of the news item.
        content_en (str): The English content of the news item.
        featured_image (str): The URL of the featured image.
        featured_image_alt (str): The alt text for the featured image.
        gallery_images (str): A JSON array of gallery image URLs.
        category_id (int): The foreign key for the news category.
        tags (relationship): A relationship to the tags associated with the news item.
        status (str): The status of the news item (e.g., 'draft', 'published', 'archived').
        is_published (bool): Whether the news item is published.
        is_featured (bool): Whether the news item is featured.
        is_breaking (bool): Whether the news item is a breaking news story.
        priority (int): The priority of the news item.
        published_at (datetime): The timestamp when the news item was published.
        expires_at (datetime): The timestamp when the news item expires.
        created_at (datetime): The timestamp when the news item was created.
        updated_at (datetime): The timestamp when the news item was last updated.
        author_id (int): The ID of the author.
        author_name (str): The name of the author.
        editor_id (int): The ID of the editor.
        view_count (int): The number of times the news item has been viewed.
        like_count (int): The number of likes the news item has received.
        share_count (int): The number of times the news item has been shared.
        comment_count (int): The number of comments on the news item.
        meta_title (str): The meta title for SEO.
        meta_description (str): The meta description for SEO.
        meta_keywords (str): The meta keywords for SEO.
        comments (relationship): A relationship to the comments on the news item.
        stats (relationship): A relationship to the statistics for the news item.
    """
    __tablename__ = 'news_items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200))
    slug = db.Column(db.String(250), unique=True, nullable=False)
    summary = db.Column(db.Text)
    summary_en = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text)

    # Images and media
    featured_image = db.Column(db.String(500))
    featured_image_alt = db.Column(db.String(200))
    gallery_images = db.Column(db.Text)  # JSON array

    # Category and tags
    category_id = db.Column(db.Integer, db.ForeignKey('news_categories.id'), nullable=False)
    tags = db.relationship('NewsTag', secondary=news_tags_association, backref='news_items')

    # Status and publishing
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_breaking = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=0)

    # Timestamps
    published_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Author and editor
    author_id = db.Column(db.Integer)
    author_name = db.Column(db.String(100))
    editor_id = db.Column(db.Integer)

    # Statistics
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)

    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    meta_keywords = db.Column(db.String(500))

    # Relationships
    comments = db.relationship('NewsComment', backref='news_item', lazy='dynamic', cascade='all, delete-orphan')
    stats = db.relationship('NewsStats', backref='news_item', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<NewsItem {self.title}>'

    def is_active(self):
        """Checks if the news item is active and not expired."""
        if not self.is_published:
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        return True

    def increment_view_count(self):
        """Increments the view count of the news item."""
        self.view_count += 1
        db.session.commit()

    def get_gallery_images(self):
        """Returns the gallery images as a list."""
        if self.gallery_images:
            try:
                return json.loads(self.gallery_images)
            except:
                return []
        return []

    def set_gallery_images(self, images):
        """Sets the gallery images from a list."""
        self.gallery_images = json.dumps(images) if images else None

    def to_dict(self, include_content=False):
        """Serializes the object to a dictionary."""
        data = {
            'id': self.id,
            'title': self.title,
            'title_en': self.title_en,
            'slug': self.slug,
            'summary': self.summary,
            'summary_en': self.summary_en,
            'featured_image': self.featured_image,
            'featured_image_alt': self.featured_image_alt,
            'gallery_images': self.get_gallery_images(),
            'category': self.category.to_dict() if self.category else None,
            'tags': [tag.to_dict() for tag in self.tags],
            'status': self.status,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'is_breaking': self.is_breaking,
            'priority': self.priority,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'author_name': self.author_name,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'share_count': self.share_count,
            'comment_count': self.comment_count,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'is_active': self.is_active()
        }

        if include_content:
            data.update({
                'content': self.content,
                'content_en': self.content_en
            })

        return data


class NewsComment(db.Model):
    """Represents a comment on a news item.

    Attributes:
        id (int): The primary key.
        news_item_id (int): The foreign key for the news item.
        user_id (int): The ID of the user who made the comment.
        user_name (str): The name of the user.
        user_email (str): The email of the user.
        user_ip (str): The IP address of the user.
        content (str): The content of the comment.
        parent_id (int): The ID of the parent comment for replies.
        is_approved (bool): Whether the comment is approved.
        is_spam (bool): Whether the comment is marked as spam.
        is_deleted (bool): Whether the comment is deleted.
        created_at (datetime): The timestamp when the comment was created.
        approved_at (datetime): The timestamp when the comment was approved.
        approved_by (int): The ID of the admin who approved the comment.
        replies (relationship): A relationship to the replies to this comment.
    """
    __tablename__ = 'news_comments'

    id = db.Column(db.Integer, primary_key=True)
    news_item_id = db.Column(db.Integer, db.ForeignKey('news_items.id'), nullable=False)

    # Commenter information
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(150))
    user_ip = db.Column(db.String(45))

    # Content
    content = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('news_comments.id'))  # For replies

    # Status
    is_approved = db.Column(db.Boolean, default=False)
    is_spam = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer)

    # Relationships
    replies = db.relationship('NewsComment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return f'<NewsComment {self.id} by {self.user_name}>'

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            'id': self.id,
            'news_item_id': self.news_item_id,
            'user_name': self.user_name,
            'content': self.content,
            'parent_id': self.parent_id,
            'is_approved': self.is_approved,
            'is_spam': self.is_spam,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'replies_count': self.replies.filter_by(is_approved=True, is_deleted=False).count()
        }


class NewsStats(db.Model):
    """Represents daily statistics for a news item.

    Attributes:
        id (int): The primary key.
        news_item_id (int): The foreign key for the news item.
        date (date): The date of the statistics.
        views (int): The number of views.
        unique_views (int): The number of unique views.
        likes (int): The number of likes.
        shares (int): The number of shares.
        comments (int): The number of comments.
        avg_read_time (float): The average read time in seconds.
        bounce_rate (float): The bounce rate.
        engagement_rate (float): The engagement rate.
        direct_visits (int): The number of direct visits.
        social_visits (int): The number of visits from social media.
        search_visits (int): The number of visits from search engines.
        referral_visits (int): The number of referral visits.
        created_at (datetime): The timestamp when the stats were created.
    """
    __tablename__ = 'news_stats'

    id = db.Column(db.Integer, primary_key=True)
    news_item_id = db.Column(db.Integer, db.ForeignKey('news_items.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Statistics
    views = db.Column(db.Integer, default=0)
    unique_views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)

    # Engagement metrics
    avg_read_time = db.Column(db.Float, default=0.0)  # in seconds
    bounce_rate = db.Column(db.Float, default=0.0)
    engagement_rate = db.Column(db.Float, default=0.0)

    # Traffic sources
    direct_visits = db.Column(db.Integer, default=0)
    social_visits = db.Column(db.Integer, default=0)
    search_visits = db.Column(db.Integer, default=0)
    referral_visits = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('news_item_id', 'date', name='unique_news_date_stats'),)

    def __repr__(self):
        return f'<NewsStats {self.news_item_id} - {self.date}>'

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            'id': self.id,
            'news_item_id': self.news_item_id,
            'date': self.date.isoformat() if self.date else None,
            'views': self.views,
            'unique_views': self.unique_views,
            'likes': self.likes,
            'shares': self.shares,
            'comments': self.comments,
            'avg_read_time': self.avg_read_time,
            'bounce_rate': self.bounce_rate,
            'engagement_rate': self.engagement_rate,
            'direct_visits': self.direct_visits,
            'social_visits': self.social_visits,
            'search_visits': self.search_visits,
            'referral_visits': self.referral_visits,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class NewsSettings(db.Model):
    """Represents settings for the news service.

    This model stores key-value settings for the news service, allowing for dynamic configuration.

    Attributes:
        id (int): The primary key.
        setting_key (str): The unique key for the setting.
        setting_value (str): The value of the setting.
        setting_type (str): The data type of the setting (e.g., 'string', 'integer', 'boolean', 'json').
        description (str): A description of the setting.
        category (str): The category of the setting (e.g., 'general', 'seo').
        is_public (bool): Whether the setting is public and can be exposed via an API.
        created_at (datetime): The timestamp when the setting was created.
        updated_at (datetime): The timestamp when the setting was last updated.
    """
    __tablename__ = 'news_settings'

    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(20), default='string')  # string, integer, boolean, json
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='general')
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<NewsSettings {self.setting_key}>'

    def get_value(self):
        """Returns the setting value in the correct data type."""
        if self.setting_type == 'integer':
            return int(self.setting_value) if self.setting_value else 0
        elif self.setting_type == 'boolean':
            return self.setting_value.lower() == 'true' if self.setting_value else False
        elif self.setting_type == 'json':
            try:
                return json.loads(self.setting_value) if self.setting_value else {}
            except:
                return {}
        else:
            return self.setting_value or ''

    def set_value(self, value):
        """Sets the setting value in the correct data type."""
        if self.setting_type == 'json':
            self.setting_value = json.dumps(value)
        else:
            self.setting_value = str(value)

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            'id': self.id,
            'setting_key': self.setting_key,
            'setting_value': self.get_value(),
            'setting_type': self.setting_type,
            'description': self.description,
            'category': self.category,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Create indexes for performance optimization
db.Index('idx_news_published', NewsItem.is_published, NewsItem.published_at)
db.Index('idx_news_category', NewsItem.category_id, NewsItem.is_published)
db.Index('idx_news_featured', NewsItem.is_featured, NewsItem.priority)
db.Index('idx_news_breaking', NewsItem.is_breaking, NewsItem.created_at)
db.Index('idx_news_slug', NewsItem.slug)
db.Index('idx_comments_approved', NewsComment.is_approved, NewsComment.created_at)
db.Index('idx_stats_date', NewsStats.date, NewsStats.news_item_id)
'''
