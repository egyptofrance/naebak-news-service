"""
نماذج خدمة الأخبار - مشروع نائبك
Flask + SQLite Models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()


class NewsCategory(db.Model):
    """تصنيفات الأخبار"""
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
    
    # العلاقات
    news_items = db.relationship('NewsItem', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<NewsCategory {self.name}>'
    
    def to_dict(self):
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
    """علامات الأخبار"""
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


# جدول الربط بين الأخبار والعلامات
news_tags_association = db.Table('news_item_tags',
    db.Column('news_item_id', db.Integer, db.ForeignKey('news_items.id'), primary_key=True),
    db.Column('news_tag_id', db.Integer, db.ForeignKey('news_tags.id'), primary_key=True)
)


class NewsItem(db.Model):
    """الأخبار والمقالات"""
    __tablename__ = 'news_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200))
    slug = db.Column(db.String(250), unique=True, nullable=False)
    summary = db.Column(db.Text)
    summary_en = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text)
    
    # الصور والوسائط
    featured_image = db.Column(db.String(500))
    featured_image_alt = db.Column(db.String(200))
    gallery_images = db.Column(db.Text)  # JSON array
    
    # التصنيف والعلامات
    category_id = db.Column(db.Integer, db.ForeignKey('news_categories.id'), nullable=False)
    tags = db.relationship('NewsTag', secondary=news_tags_association, backref='news_items')
    
    # الحالة والنشر
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_breaking = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=0)
    
    # التواريخ
    published_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # المؤلف والمحرر
    author_id = db.Column(db.Integer)
    author_name = db.Column(db.String(100))
    editor_id = db.Column(db.Integer)
    
    # الإحصائيات
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    
    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    meta_keywords = db.Column(db.String(500))
    
    # العلاقات
    comments = db.relationship('NewsComment', backref='news_item', lazy='dynamic', cascade='all, delete-orphan')
    stats = db.relationship('NewsStats', backref='news_item', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<NewsItem {self.title}>'
    
    def is_active(self):
        """التحقق من أن الخبر نشط ولم ينته"""
        if not self.is_published:
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        return True
    
    def increment_view_count(self):
        """زيادة عدد المشاهدات"""
        self.view_count += 1
        db.session.commit()
    
    def get_gallery_images(self):
        """الحصول على صور المعرض"""
        if self.gallery_images:
            try:
                return json.loads(self.gallery_images)
            except:
                return []
        return []
    
    def set_gallery_images(self, images):
        """تعيين صور المعرض"""
        self.gallery_images = json.dumps(images) if images else None
    
    def to_dict(self, include_content=False):
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
    """تعليقات الأخبار"""
    __tablename__ = 'news_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    news_item_id = db.Column(db.Integer, db.ForeignKey('news_items.id'), nullable=False)
    
    # معلومات المعلق
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(150))
    user_ip = db.Column(db.String(45))
    
    # المحتوى
    content = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('news_comments.id'))  # للردود
    
    # الحالة
    is_approved = db.Column(db.Boolean, default=False)
    is_spam = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # التواريخ
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer)
    
    # العلاقات
    replies = db.relationship('NewsComment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    def __repr__(self):
        return f'<NewsComment {self.id} by {self.user_name}>'
    
    def to_dict(self):
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
    """إحصائيات الأخبار اليومية"""
    __tablename__ = 'news_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    news_item_id = db.Column(db.Integer, db.ForeignKey('news_items.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # الإحصائيات
    views = db.Column(db.Integer, default=0)
    unique_views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    
    # معدلات التفاعل
    avg_read_time = db.Column(db.Float, default=0.0)  # بالثواني
    bounce_rate = db.Column(db.Float, default=0.0)
    engagement_rate = db.Column(db.Float, default=0.0)
    
    # مصادر الزيارات
    direct_visits = db.Column(db.Integer, default=0)
    social_visits = db.Column(db.Integer, default=0)
    search_visits = db.Column(db.Integer, default=0)
    referral_visits = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('news_item_id', 'date', name='unique_news_date_stats'),)
    
    def __repr__(self):
        return f'<NewsStats {self.news_item_id} - {self.date}>'
    
    def to_dict(self):
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
    """إعدادات خدمة الأخبار"""
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
        """الحصول على القيمة بالنوع الصحيح"""
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
        """تعيين القيمة بالنوع الصحيح"""
        if self.setting_type == 'json':
            self.setting_value = json.dumps(value)
        else:
            self.setting_value = str(value)
    
    def to_dict(self):
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


# إنشاء فهارس لتحسين الأداء
db.Index('idx_news_published', NewsItem.is_published, NewsItem.published_at)
db.Index('idx_news_category', NewsItem.category_id, NewsItem.is_published)
db.Index('idx_news_featured', NewsItem.is_featured, NewsItem.priority)
db.Index('idx_news_breaking', NewsItem.is_breaking, NewsItem.created_at)
db.Index('idx_news_slug', NewsItem.slug)
db.Index('idx_comments_approved', NewsComment.is_approved, NewsComment.created_at)
db.Index('idx_stats_date', NewsStats.date, NewsStats.news_item_id)
