# 🏷️ خدمة الأخبار (naebak-news-service)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/egyptofrance/naebak-news-service/actions)
[![Coverage](https://img.shields.io/badge/coverage-90%25-green)](https://github.com/egyptofrance/naebak-news-service)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/egyptofrance/naebak-news-service/releases)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

## 📝 الوصف

خدمة تجميع وعرض الأخبار المتعلقة بالنواب والبرلمان. تقوم الخدمة بجمع الأخبار من مصادر متعددة، تصنيفها، وتوفيرها للمستخدمين من خلال واجهة برمجة تطبيقات (API).

---

## ✨ الميزات الرئيسية

- **تجميع الأخبار**: جمع الأخبار من مصادر إخبارية متنوعة.
- **تصنيف الأخبار**: تصنيف الأخبار حسب الموضوع والنائب.
- **بحث متقدم**: إمكانية البحث في الأخبار باستخدام كلمات مفتاحية.
- **تنبيهات الأخبار**: إرسال تنبيهات للمستخدمين بالأخبار الهامة.

---

## 🛠️ التقنيات المستخدمة

| التقنية | الإصدار | الغرض |
|---------|---------|-------|
| **Django** | 4.2.5 | إطار العمل الأساسي |
| **Django REST Framework** | 3.14.0 | تطوير APIs |
| **PostgreSQL** | 13+ | قاعدة البيانات الرئيسية |
| **Beautiful Soup** | 4.12.2 | استخلاص البيانات من الويب |
| **Celery** | 5.3+ | جدولة مهام تجميع الأخبار |

---

## 🚀 التثبيت والتشغيل

```bash
git clone https://github.com/egyptofrance/naebak-news-service.git
cd naebak-news-service

# اتبع نفس خطوات التثبيت والتشغيل لباقي خدمات Django
```

---

## 📚 توثيق الـ API

- **Swagger UI**: [http://localhost:8003/api/docs/](http://localhost:8003/api/docs/)

---

## 🤝 المساهمة

يرجى مراجعة [دليل المساهمة](CONTRIBUTING.md) و [معايير التوثيق الموحدة](../../naebak-almakhzan/DOCUMENTATION_STANDARDS.md).

---

## 📄 الترخيص

هذا المشروع مرخص تحت [رخصة MIT](LICENSE).

