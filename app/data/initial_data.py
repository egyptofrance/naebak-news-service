"""
البيانات الأساسية لخدمة الأخبار - مشروع نائبك
"""
from datetime import datetime, timedelta

# تصنيفات الأخبار
NEWS_CATEGORIES = [
    {
        'name': 'أخبار سياسية',
        'name_en': 'Political News',
        'description': 'أخبار متعلقة بالسياسة والحكومة والقرارات السياسية',
        'description_en': 'News related to politics, government and political decisions',
        'icon': '🏛️',
        'color': '#007BFF',
        'display_order': 1
    },
    {
        'name': 'أخبار اقتصادية',
        'name_en': 'Economic News',
        'description': 'أخبار الاقتصاد والمال والأعمال والاستثمار',
        'description_en': 'Economy, finance, business and investment news',
        'icon': '💰',
        'color': '#28A745',
        'display_order': 2
    },
    {
        'name': 'أخبار اجتماعية',
        'name_en': 'Social News',
        'description': 'أخبار المجتمع والقضايا الاجتماعية والثقافية',
        'description_en': 'Community, social and cultural issues news',
        'icon': '👥',
        'color': '#17A2B8',
        'display_order': 3
    },
    {
        'name': 'أخبار محلية',
        'name_en': 'Local News',
        'description': 'أخبار المحافظات والمناطق المحلية',
        'description_en': 'Governorates and local areas news',
        'icon': '🏘️',
        'color': '#FFC107',
        'display_order': 4
    },
    {
        'name': 'أخبار برلمانية',
        'name_en': 'Parliamentary News',
        'description': 'أخبار البرلمان والنواب والقوانين',
        'description_en': 'Parliament, representatives and legislation news',
        'icon': '⚖️',
        'color': '#6F42C1',
        'display_order': 5
    },
    {
        'name': 'أخبار عامة',
        'name_en': 'General News',
        'description': 'أخبار متنوعة وعامة',
        'description_en': 'Various and general news',
        'icon': '📰',
        'color': '#6C757D',
        'display_order': 6
    }
]

# علامات الأخبار
NEWS_TAGS = [
    {'name': 'عاجل', 'name_en': 'Breaking', 'description': 'أخبار عاجلة ومهمة', 'color': '#DC3545'},
    {'name': 'مهم', 'name_en': 'Important', 'description': 'أخبار مهمة للمتابعة', 'color': '#FD7E14'},
    {'name': 'تحديث', 'name_en': 'Update', 'description': 'تحديثات على أخبار سابقة', 'color': '#20C997'},
    {'name': 'تحليل', 'name_en': 'Analysis', 'description': 'تحليلات وآراء', 'color': '#6F42C1'},
    {'name': 'مقابلة', 'name_en': 'Interview', 'description': 'مقابلات مع شخصيات مهمة', 'color': '#17A2B8'},
    {'name': 'تقرير', 'name_en': 'Report', 'description': 'تقارير مفصلة', 'color': '#28A745'},
    {'name': 'إعلان', 'name_en': 'Announcement', 'description': 'إعلانات رسمية', 'color': '#007BFF'},
    {'name': 'فعالية', 'name_en': 'Event', 'description': 'فعاليات ومؤتمرات', 'color': '#E83E8C'},
    {'name': 'قانون', 'name_en': 'Law', 'description': 'قوانين وتشريعات', 'color': '#6C757D'},
    {'name': 'انتخابات', 'name_en': 'Elections', 'description': 'أخبار الانتخابات', 'color': '#FFC107'}
]

# أخبار تجريبية
SAMPLE_NEWS = [
    {
        'title': 'مجلس النواب يناقش قانون جديد لتطوير التعليم',
        'title_en': 'Parliament Discusses New Education Development Law',
        'slug': 'parliament-education-law-discussion',
        'summary': 'يناقش مجلس النواب اليوم مشروع قانون جديد يهدف إلى تطوير منظومة التعليم في مصر وتحسين جودة التعليم.',
        'summary_en': 'Parliament discusses today a new bill aimed at developing the education system in Egypt and improving education quality.',
        'content': '''
يناقش مجلس النواب المصري اليوم مشروع قانون جديد يهدف إلى تطوير منظومة التعليم في مصر وتحسين جودة التعليم على جميع المستويات.

## أهداف القانون الجديد

يتضمن مشروع القانون عدة محاور رئيسية:

### 1. تطوير المناهج
- تحديث المناهج الدراسية لتواكب التطورات العالمية
- إدخال التكنولوجيا في العملية التعليمية
- التركيز على المهارات العملية والتطبيقية

### 2. تأهيل المعلمين
- برامج تدريبية متقدمة للمعلمين
- رفع مستوى الأجور والحوافز
- نظام تقييم شامل للأداء

### 3. تطوير البنية التحتية
- بناء مدارس جديدة بمعايير عالمية
- تجهيز المدارس بأحدث التقنيات
- تحسين البيئة التعليمية

## آراء النواب

أعرب عدد من النواب عن تأييدهم للمشروع، مؤكدين أهمية الاستثمار في التعليم كأساس للتنمية المستدامة.

من جانب آخر، طالب بعض النواب بضرورة توفير الميزانية اللازمة لتنفيذ هذه الخطط الطموحة.

## الخطوات التالية

من المتوقع أن يتم التصويت على مشروع القانون خلال الجلسات القادمة، بعد استكمال المناقشات والتعديلات المطلوبة.
        ''',
        'category_name': 'أخبار برلمانية',
        'tags': ['مهم', 'قانون', 'تقرير'],
        'is_published': True,
        'is_featured': True,
        'priority': 5,
        'author_name': 'أحمد محمد',
        'view_count': 1250,
        'like_count': 89,
        'share_count': 34,
        'published_at': datetime.now() - timedelta(hours=2)
    },
    {
        'title': 'النائب سارة أحمد تطلق مبادرة لدعم المرأة العاملة',
        'title_en': 'MP Sara Ahmed Launches Initiative to Support Working Women',
        'slug': 'sara-ahmed-working-women-initiative',
        'summary': 'أطلقت النائب سارة أحمد مبادرة جديدة لدعم المرأة العاملة وتوفير فرص عمل مناسبة للأمهات.',
        'summary_en': 'MP Sara Ahmed launched a new initiative to support working women and provide suitable job opportunities for mothers.',
        'content': '''
أطلقت النائب سارة أحمد، عضو مجلس النواب عن دائرة الجيزة، مبادرة جديدة تحت عنوان "المرأة قوة الوطن" لدعم المرأة العاملة في مصر.

## أهداف المبادرة

تهدف المبادرة إلى:

- توفير فرص عمل مرنة للأمهات
- تدريب النساء على المهارات الرقمية
- دعم المشاريع الصغيرة للنساء
- توفير حضانات في أماكن العمل

## التفاصيل

تتضمن المبادرة شراكات مع:
- الشركات الكبرى لتوفير فرص العمل المرن
- مراكز التدريب المهني
- البنوك لتمويل المشاريع الصغيرة
- منظمات المجتمع المدني

## ردود الفعل

لقيت المبادرة ترحيباً واسعاً من المواطنين ومنظمات المجتمع المدني، حيث أشادوا بالجهود المبذولة لدعم المرأة المصرية.

من المتوقع أن تستفيد آلاف النساء من هذه المبادرة خلال العام الجاري.
        ''',
        'category_name': 'أخبار اجتماعية',
        'tags': ['مهم', 'فعالية', 'إعلان'],
        'is_published': True,
        'is_featured': False,
        'priority': 3,
        'author_name': 'فاطمة علي',
        'view_count': 890,
        'like_count': 156,
        'share_count': 67,
        'published_at': datetime.now() - timedelta(hours=6)
    },
    {
        'title': 'عاجل: اجتماع طارئ للجنة الاقتصادية بالبرلمان',
        'title_en': 'Breaking: Emergency Meeting of Parliamentary Economic Committee',
        'slug': 'emergency-economic-committee-meeting',
        'summary': 'تعقد اللجنة الاقتصادية بمجلس النواب اجتماعاً طارئاً لمناقشة التطورات الاقتصادية الأخيرة.',
        'summary_en': 'The Economic Committee of Parliament holds an emergency meeting to discuss recent economic developments.',
        'content': '''
تعقد اللجنة الاقتصادية بمجلس النواب اجتماعاً طارئاً اليوم لمناقشة التطورات الاقتصادية الأخيرة وتأثيرها على الاقتصاد المصري.

## جدول الأعمال

يتضمن جدول أعمال الاجتماع:

1. مراجعة المؤشرات الاقتصادية الحالية
2. مناقشة تأثير التطورات العالمية
3. اقتراح حلول لدعم الاقتصاد المحلي
4. مراجعة السياسات النقدية والمالية

## الحضور

يحضر الاجتماع:
- أعضاء اللجنة الاقتصادية
- ممثلون عن وزارة المالية
- ممثلون عن البنك المركزي
- خبراء اقتصاديون

## التوقعات

من المتوقع أن يخرج الاجتماع بتوصيات مهمة لدعم الاقتصاد المصري ومواجهة التحديات الراهنة.

سيتم الإعلان عن نتائج الاجتماع في مؤتمر صحفي مساء اليوم.
        ''',
        'category_name': 'أخبار اقتصادية',
        'tags': ['عاجل', 'مهم', 'تحديث'],
        'is_published': True,
        'is_featured': True,
        'is_breaking': True,
        'priority': 10,
        'author_name': 'محمد حسن',
        'view_count': 2340,
        'like_count': 198,
        'share_count': 145,
        'published_at': datetime.now() - timedelta(minutes=30)
    },
    {
        'title': 'محافظ القاهرة يفتتح مشروع تطوير الطرق الجديد',
        'title_en': 'Cairo Governor Opens New Road Development Project',
        'slug': 'cairo-road-development-project',
        'summary': 'افتتح محافظ القاهرة اليوم مشروع تطوير الطرق الجديد الذي يهدف إلى تحسين حركة المرور في العاصمة.',
        'summary_en': 'Cairo Governor today opened the new road development project aimed at improving traffic flow in the capital.',
        'content': '''
افتتح محافظ القاهرة اليوم مشروع تطوير الطرق الجديد في منطقة مصر الجديدة، والذي يأتي ضمن خطة شاملة لتحسين البنية التحتية في العاصمة.

## تفاصيل المشروع

يشمل المشروع:
- تطوير 15 كيلومتر من الطرق الرئيسية
- إنشاء 3 كباري علوية جديدة
- تركيب نظام إشارات مرور ذكي
- إنشاء ممرات للدراجات

## التكلفة والتمويل

بلغت تكلفة المشروع 500 مليون جنيه، وتم تمويله من:
- الموازنة العامة للدولة (60%)
- القروض الميسرة (40%)

## الفوائد المتوقعة

من المتوقع أن يحقق المشروع:
- تقليل زمن الانتقال بنسبة 30%
- تحسين جودة الهواء
- زيادة السلامة المرورية
- دعم النشاط الاقتصادي في المنطقة

## المرحلة التالية

أعلن المحافظ عن بدء المرحلة الثانية من المشروع العام القادم، والتي ستشمل مناطق أخرى في القاهرة.
        ''',
        'category_name': 'أخبار محلية',
        'tags': ['فعالية', 'تقرير', 'إعلان'],
        'is_published': True,
        'is_featured': False,
        'priority': 2,
        'author_name': 'علي السيد',
        'view_count': 567,
        'like_count': 43,
        'share_count': 21,
        'published_at': datetime.now() - timedelta(hours=12)
    },
    {
        'title': 'مؤتمر صحفي لوزير الصحة حول تطوير المستشفيات',
        'title_en': 'Health Minister Press Conference on Hospital Development',
        'slug': 'health-minister-hospital-development',
        'summary': 'عقد وزير الصحة مؤتمراً صحفياً للإعلان عن خطة شاملة لتطوير المستشفيات الحكومية.',
        'summary_en': 'Health Minister held a press conference to announce a comprehensive plan for developing government hospitals.',
        'content': '''
عقد وزير الصحة والسكان مؤتمراً صحفياً اليوم للإعلان عن خطة شاملة لتطوير المستشفيات الحكومية على مستوى الجمهورية.

## محاور الخطة

تتضمن الخطة عدة محاور:

### 1. التطوير التقني
- تحديث الأجهزة الطبية
- إدخال تقنيات الذكاء الاصطناعي
- نظام إدارة المستشفيات الإلكتروني

### 2. تأهيل الكوادر
- برامج تدريبية للأطباء والممرضين
- ابتعاث للخارج للتخصصات النادرة
- رفع مستوى الأجور والحوافز

### 3. البنية التحتية
- بناء مستشفيات جديدة
- توسيع المستشفيات الحالية
- تحسين الخدمات المساندة

## الميزانية

خصصت الدولة 10 مليارات جنيه لتنفيذ هذه الخطة على مدى 3 سنوات.

## الجدول الزمني

- السنة الأولى: تطوير 50 مستشفى
- السنة الثانية: تطوير 75 مستشفى
- السنة الثالثة: استكمال باقي المستشفيات

## ردود الفعل

أشاد الأطباء والمواطنون بهذه الخطة الطموحة، معربين عن أملهم في تحسين الخدمات الصحية.
        ''',
        'category_name': 'أخبار عامة',
        'tags': ['مقابلة', 'إعلان', 'مهم'],
        'is_published': True,
        'is_featured': False,
        'priority': 4,
        'author_name': 'نورا إبراهيم',
        'view_count': 1120,
        'like_count': 87,
        'share_count': 52,
        'published_at': datetime.now() - timedelta(days=1)
    }
]

# تعليقات تجريبية
SAMPLE_COMMENTS = [
    {
        'news_slug': 'parliament-education-law-discussion',
        'user_name': 'أحمد محمود',
        'user_email': 'ahmed@example.com',
        'content': 'مبادرة ممتازة، نحتاج فعلاً لتطوير التعليم في مصر. أتمنى أن يتم التنفيذ بشكل صحيح.',
        'is_approved': True
    },
    {
        'news_slug': 'parliament-education-law-discussion',
        'user_name': 'فاطمة علي',
        'user_email': 'fatma@example.com',
        'content': 'المهم هو التطبيق الفعلي وليس مجرد القوانين. نريد أن نرى نتائج ملموسة.',
        'is_approved': True
    },
    {
        'news_slug': 'sara-ahmed-working-women-initiative',
        'user_name': 'مريم حسن',
        'user_email': 'mariam@example.com',
        'content': 'مبادرة رائعة من النائب سارة أحمد. المرأة المصرية تستحق كل الدعم.',
        'is_approved': True
    },
    {
        'news_slug': 'emergency-economic-committee-meeting',
        'user_name': 'محمد عبدالله',
        'user_email': 'mohamed@example.com',
        'content': 'نتطلع لمعرفة نتائج الاجتماع وما سيتم اتخاذه من قرارات لدعم الاقتصاد.',
        'is_approved': True
    },
    {
        'news_slug': 'cairo-road-development-project',
        'user_name': 'سارة أحمد',
        'user_email': 'sara@example.com',
        'content': 'أخيراً! كنا في حاجة ماسة لتطوير الطرق في هذه المنطقة. شكراً للمحافظ.',
        'is_approved': True
    }
]

# إعدادات النظام
NEWS_SETTINGS = [
    {
        'setting_key': 'news_per_page',
        'setting_value': '10',
        'setting_type': 'integer',
        'description': 'عدد الأخبار في الصفحة الواحدة',
        'category': 'display'
    },
    {
        'setting_key': 'featured_news_count',
        'setting_value': '5',
        'setting_type': 'integer',
        'description': 'عدد الأخبار المميزة في الصفحة الرئيسية',
        'category': 'display'
    },
    {
        'setting_key': 'breaking_news_duration',
        'setting_value': '24',
        'setting_type': 'integer',
        'description': 'مدة عرض الأخبار العاجلة بالساعات',
        'category': 'content'
    },
    {
        'setting_key': 'auto_archive_days',
        'setting_value': '365',
        'setting_type': 'integer',
        'description': 'عدد الأيام قبل الأرشفة التلقائية',
        'category': 'content'
    },
    {
        'setting_key': 'comments_enabled',
        'setting_value': 'true',
        'setting_type': 'boolean',
        'description': 'تفعيل نظام التعليقات',
        'category': 'interaction'
    },
    {
        'setting_key': 'comments_moderation',
        'setting_value': 'true',
        'setting_type': 'boolean',
        'description': 'مراجعة التعليقات قبل النشر',
        'category': 'interaction'
    },
    {
        'setting_key': 'max_comment_length',
        'setting_value': '500',
        'setting_type': 'integer',
        'description': 'الحد الأقصى لطول التعليق',
        'category': 'interaction'
    },
    {
        'setting_key': 'site_name',
        'setting_value': 'نائبك - أخبار',
        'setting_type': 'string',
        'description': 'اسم الموقع',
        'category': 'general',
        'is_public': True
    },
    {
        'setting_key': 'contact_email',
        'setting_value': 'news@naebak.com',
        'setting_type': 'string',
        'description': 'بريد التواصل',
        'category': 'general',
        'is_public': True
    },
    {
        'setting_key': 'social_sharing',
        'setting_value': 'true',
        'setting_type': 'boolean',
        'description': 'تفعيل مشاركة الأخبار على وسائل التواصل',
        'category': 'social',
        'is_public': True
    }
]

# إحصائيات تجريبية (آخر 7 أيام)
def generate_sample_stats():
    """إنشاء إحصائيات تجريبية لآخر 7 أيام"""
    stats = []
    base_date = datetime.now().date()
    
    for i in range(7):
        date = base_date - timedelta(days=i)
        for news_id in range(1, 6):  # للأخبار الـ 5 التجريبية
            stat = {
                'news_item_id': news_id,
                'date': date,
                'views': max(50, 200 - (i * 20) + (news_id * 10)),
                'unique_views': max(30, 150 - (i * 15) + (news_id * 8)),
                'likes': max(5, 20 - (i * 2) + news_id),
                'shares': max(2, 10 - i + news_id),
                'comments': max(1, 5 - i + (news_id // 2)),
                'avg_read_time': 120.0 + (news_id * 30),
                'bounce_rate': 0.3 + (i * 0.05),
                'engagement_rate': 0.15 - (i * 0.02),
                'direct_visits': max(10, 50 - (i * 5)),
                'social_visits': max(5, 30 - (i * 3)),
                'search_visits': max(8, 40 - (i * 4)),
                'referral_visits': max(3, 15 - (i * 2))
            }
            stats.append(stat)
    
    return stats

SAMPLE_STATS = generate_sample_stats()
