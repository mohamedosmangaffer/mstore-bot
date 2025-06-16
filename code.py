MstoreBot/
├── bot/
│   ├── handlers/
│   │   ├── start.py
│   │   ├── language.py
│   │   ├── menu.py
│   │   ├── orders.py
│   │   └── admin.py          # (اختياري - لإدارة خاصة مستقبلاً)
│   ├── db/
│   │   └── database.py       # إعداد SQLite
│   ├── middleware/
│   │   └── rate_limiter.py   # مانع السبام
│   ├── utils/
│   │   └── translator.py     # (قابل للتوسعة لدعم لغات إضافية)
│   ├── receipts/             # مجلد لحفظ صور إثبات الدفع
│   └── main.py               # ملف التشغيل الرئيسي
├── dashboard/                # لوحة تحكم ويب (FastAPI)
│   ├── app.py
│   ├── templates/
│   │   └── orders.html       # واجهة HTML للطلبات
│   ├── static/
│   │   └── style.css         # تنسيق الواجهة (اختياري)
├── orders.db                 # قاعدة البيانات SQLite
├── .env                      # ملف الإعدادات (BOT_TOKEN + ADMIN_ID)
├── requirements.txt          # تبعيات المشروع
└── README.md                 # توثيق المشروع
