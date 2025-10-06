# Channel-Manager
🤖 Smart channel &amp; group manager — automate posts, monitor stats, control members.  ⚙️ Automate posting, analytics and member control for channels &amp; groups. Secure and fast.  📊 Channel &amp; group admin assistant: scheduling, analytics, moderation — fast and reliable.


# 🤖 Telegram Kanal Boshqaruv Boti

Telegram kanallar va guruhlarni to'liq boshqarish uchun mo'ljallangan professional bot. Bu bot orqali bir nechta kanallaringizni bitta joydan boshqarishingiz, xabarlar yuborishingiz, a'zolarni nazorat qilishingiz va boshqa ko'plab imkoniyatlardan foydalanishingiz mumkin.


## ✨ Xususiyatlar

### 📢 Kanal Boshqaruvi
- ✅ Bir nechta kanal/guruhni qo'shish va boshqarish
- ✅ Kanal nomini va tavsifini o'zgartirish
- ✅ Kanal rasmini o'rnatish va o'chirish
- ✅ Kanal ma'lumotlarini ko'rish (a'zolar soni, statistika)
- ✅ To'liq JSON bazasida saqlash

### 📤 Xabar Yuborish
- 💬 **Oddiy matnli xabarlar** (HTML format qo'llab-quvvatlash)
- 📸 **Bitta rasm** (caption bilan)
- 🖼 **Media guruh** (2-10 ta rasm)
- 📊 **So'rovnomalar** (cheksiz variant)
- 🔄 Barcha xabar turlarini birlashtirish

### 📌 Pin Boshqaruvi
- 📍 Xabarni pin qilish
- 🗑 Oxirgi pinni olib tashlash
- 🚫 Barcha pinlarni olib tashlash
- 🔔 Notifikatsiya bilan/siz pin qilish

### 👥 A'zolar Boshqaruvi (Guruhlar uchun)
- 🚫 **Ban** - Foydalanuvchini butunlay bloklash
- ✅ **Unban** - Blokdan chiqarish
- ⚠️ **Restrict** - Cheklash (yozish/media yuborish taqiqlanadi)
- ⭐️ **Promote** - Admin qilish (to'liq huquqlar bilan)

### 🔗 Taklif Havolalari
- 🔗 **Doimiy havola** - Cheksiz va doim faol
- ⏰ **Vaqtinchalik havola** - 24 soatlik, 100 kishi uchun

### 🛡 Admin Paneli
- 📊 **Statistika** - Foydalanuvchilar va kanallar soni
- 📋 **Loglar** - Barcha harakatlar jurnali
- 💾 **Backup** - Ma'lumotlar bazasi zaxirasi
- 📢 **Broadcast** - Barcha foydalanuvchilarga xabar yuborish

---

## 🚀 O'rnatish

### Talablar

- Python 3.10 yoki yuqori
- pip (Python package manager)
- Telegram Bot Token ([@BotFather](https://t.me/BotFather)dan)

### 1. Repositoriyani Klonlash

```bash
git clone https://github.com/yourusername/telegram-channel-manager.git
cd telegram-channel-manager
```

### 2. Virtual Muhitni Yaratish (Tavsiya etiladi)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Kerakli Kutubxonalarni O'rnatish

```bash
pip install -r requirements.txt
```

**requirements.txt fayli:**
```txt
aiogram==3.4.1
python-dotenv==1.0.0
aiohttp==3.9.1
```

---

## ⚙️ Sozlash

### 1. Bot Token Olish

1. [@BotFather](https://t.me/BotFather)ga kiring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username'ini kiriting
4. Tokenni saqlang (masalan: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Konfiguratsiya Fayli

Loyihaning ildiz papkasida `.env` fayli yarating:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=123456789
```

**Muhim:** `.env` faylini `.gitignore`ga qo'shing!

### 3. Admin ID Topish

1. [@userinfobot](https://t.me/userinfobot)ga kiring
2. Bot sizga Telegram ID'ingizni beradi
3. Bu ID'ni `.env` fayliga kiriting

---

## 🎯 Ishga Tushirish

### Oddiy Ishga Tushirish

```bash
python main.py
```

### Background'da Ishga Tushirish (Linux)

```bash
nohup python3 main.py > bot.log 2>&1 &
```

### Systemd Service (Linux Production)

`/etc/systemd/system/telegram-bot.service` fayli yarating:

```ini
[Unit]
Description=Telegram Channel Manager Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/telegram-channel-manager
ExecStart=/path/to/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ishga tushirish:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Docker (Opsional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Ishga tushirish:
```bash
docker build -t telegram-bot .
docker run -d --name telegram-bot --env-file .env telegram-bot
```

---

## 📖 Foydalanish

### Botni Ishga Tushirish

1. Telegram'da botingizni toping
2. `/start` buyrug'ini yuboring
3. Asosiy menyu ochiladi

### Kanal Qo'shish

1. **"➕ Kanal/Guruh Qo'shish"** tugmasini bosing
2. **Botni kanalingizda ADMIN qiling:**
   - Kanalga kiring
   - Settings → Administrators
   - Add Admin → Botingizni toping
   - Barcha kerakli huquqlarni bering
3. **Kanal ID yoki username yuboring:**
   - ID: `-1001234567890`
   - Username: `@mening_kanalim`
4. Bot kanalga ulanadi va ro'yxatga qo'shadi

### Kanal ID Topish

**Variant 1 - @userinfobot orqali:**
1. Kanal xabarini [@userinfobot](https://t.me/userinfobot)ga forward qiling
2. Bot sizga kanal ID'sini beradi

**Variant 2 - Web Telegram:**
1. web.telegram.org'ga kiring
2. Kanalga o'ting
3. URL'dagi raqam - bu kanal ID: `https://web.telegram.org/k/#-1001234567890`

### Xabar Yuborish

1. Kanalingizni tanlang
2. **"📤 Xabar Yuborish"** tugmasini bosing
3. Xabar turini tanlang:
   - **Oddiy matn** - HTML formatda
   - **Rasm** - Caption bilan
   - **Media guruh** - 2-10 ta rasm
   - **So'rovnoma** - Ko'p variantli

---

## 🎮 Komandalar

### Foydalanuvchi Komandasi

```
/start - 🚀 Botni ishga tushirish va asosiy menyu
```

### Admin Komandasi

```
/stats     - 📊 Bot statistikasi
/logs      - 📋 Faoliyat jurnalini yuklab olish
/backup    - 💾 Ma'lumotlar bazasi zaxirasi
/broadcast - 📢 Barcha foydalanuvchilarga xabar
/done      - ✅ Media yuborishni yakunlash
/cancel    - ❌ Amalni bekor qilish
```

### Komandalarni Menyuga Qo'yish

BotFather'da:
```
/mybots → Botingiz → Edit Bot → Edit Commands
```

Quyidagi matnni yuboring:
```
start - 🚀 Botni ishga tushirish va asosiy menyu
stats - 📊 Bot statistikasi (Admin)
logs - 📋 Faoliyat jurnalini yuklab olish (Admin)
backup - 💾 Ma'lumotlar bazasi zaxirasi (Admin)
broadcast - 📢 Barcha foydalanuvchilarga xabar (Admin)
```

---

## 👨‍💼 Admin Paneli

### Statistika (`/stats`)

```
📊 BOT STATISTIKASI

👥 Jami foydalanuvchilar: 1,234
📢 Jami kanallar: 5,678
📈 O'rtacha: 4.6 kanal/user

🏆 Top foydalanuvchi:
   User ID: 123456789
   Kanallar: 45 ta

💾 Ma'lumotlar bazasi: 245,678 bayt
📋 Loglar hajmi: 123,456 bayt
```

### Loglar (`/logs`)

Barcha foydalanuvchi harakatlarini ko'rsatadi:
- Kanal qo'shish/o'chirish
- Xabar yuborish
- Nom/tavsif o'zgartirish
- A'zolarni boshqarish

### Backup (`/backup`)

`channels.json` faylini yuklab olish imkonini beradi.

### Broadcast (`/broadcast`)

Barcha foydalanuvchilarga bir vaqtning o'zida xabar yuborish:

```
/broadcast Hurmatli foydalanuvchilar! Yangi funksiya qo'shildi.
```

---

## 🏗 Arxitektura

### Fayl Tuzilishi

```
telegram-channel-manager/
│
├── main.py              # Asosiy bot fayli
├── .env                 # Konfiguratsiya (tokenlar)
├── requirements.txt     # Python kutubxonalar
├── README.md           # Dokumentatsiya
│
├── channels.json       # Ma'lumotlar bazasi (avtomatik yaratiladi)
├── logs.txt           # Loglar fayli (avtomatik yaratiladi)
│
└── .gitignore         # Git ignore fayli
```

### Ma'lumotlar Bazasi Tuzilishi

`channels.json` fayli:
```json
{
  "123456789": [
    {
      "id": -1001234567890,
      "username": "mening_kanalim",
      "name": "Mening Kanalim",
      "type": "channel",
      "added": "2025-01-15 10:30:45"
    }
  ]
}
```

### State Machine

Bot aiogram FSM (Finite State Machine) dan foydalanadi:

- `waiting_for_channel_id` - Kanal ID kutmoqda
- `waiting_for_new_title` - Yangi nom kutmoqda
- `waiting_for_new_description` - Yangi tavsif kutmoqda
- `waiting_for_message` - Matn xabar kutmoqda
- `waiting_for_photo` - Rasm kutmoqda
- `waiting_for_media_group` - Media guruh kutmoqda
- `waiting_for_poll` - So'rovnoma kutmoqda
- `waiting_for_ban_user` - Ban qilish uchun ID kutmoqda
- `waiting_for_pin_message` - Pin qilish uchun ID kutmoqda

---

## 🔐 Xavfsizlik

### Botni Himoya Qilish

1. **Token'ni hech qachon ulashmang**
2. **`.env` faylini Git'ga qo'shmang**
3. **Admin ID'ni to'g'ri sozlang**
4. **Loglarni muntazam tekshiring**

### `.gitignore` Fayli

```gitignore
# Environment
.env
venv/
__pycache__/

# Data
channels.json
logs.txt
*.log

# IDE
.vscode/
.idea/
*.pyc
```

### Admin Huquqlari

Faqat `.env` faylidagi `ADMIN_ID` egasi quyidagi komandalarni ishlatishi mumkin:
- `/stats`
- `/logs`
- `/backup`
- `/broadcast`

---

## 🐛 Muammolarni Hal Qilish

### Bot Javob Bermayapti

**Sabab:** Token noto'g'ri yoki internet aloqasi yo'q

**Yechim:**
```bash
# Token'ni tekshiring
cat .env

# Bot ishga tushirish
python main.py
```

### "Bot Admin Emas" Xatosi

**Sabab:** Bot kanalda admin qilinmagan

**Yechim:**
1. Kanalga kiring
2. Settings → Administrators
3. Botni admin qiling
4. Barcha huquqlarni bering

### "Kanal Topilmadi" Xatosi

**Sabab:** Kanal ID noto'g'ri yoki bot kanalga kirish huquqiga ega emas

**Yechim:**
1. Kanal ID'ni qayta tekshiring
2. Botni kanalga a'zo qiling
3. Qaytadan urinib ko'ring

### Ma'lumotlar Yo'qoldi

**Yechim:**
```bash
# Backup'dan tiklash
cp channels.json.backup channels.json
python main.py
```

### Bot Sekin Ishlayapti

**Yechim:**
```bash
# Loglarni tozalash
> logs.txt

# Ma'lumotlar bazasini optimallashtirish
python -c "import json; data=json.load(open('channels.json')); print(len(data))"
```

---

## 🤝 Hissa Qo'shish

Botni yaxshilashga yordam bering!

### Pull Request Yuborish

1. Fork qiling
2. Yangi branch yarating: `git checkout -b feature/yangi-funksiya`
3. O'zgarishlar kiriting: `git commit -m "Yangi funksiya qo'shildi"`
4. Push qiling: `git push origin feature/yangi-funksiya`
5. Pull Request oching

### Bug Report

GitHub Issues bo'limida xato haqida xabar bering:
- Xato tavsifi
- Qadam-baqadam takrorlash yo'li
- Kutilgan va haqiqiy natija
- Screenshotlar (agar kerak bo'lsa)

---

## 📝 Litsenziya

MIT License

```
Copyright (c) 2025 [Sizning Ismingiz]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 📞 Aloqa

- **Telegram:** [@bynoutbook](https://t.me/bynoutbook)
- **GitHub:** [github.com/Baydjayev](https://github.com/Baydjayev)
- **Email:** ippark96@gmail.com

---

## 🙏 Minnatdorchilik

- [aiogram](https://docs.aiogram.dev/) - Telegram Bot Framework
- [Telegram Bot API](https://core.telegram.org/bots/api) - Official API
- Barcha foydalanuvchilar va contributorlar

---

## 📚 Qo'shimcha Resurslar

- [Telegram Bot API Dokumentatsiya](https://core.telegram.org/bots/api)
- [aiogram Dokumentatsiya](https://docs.aiogram.dev/en/latest/)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [Telegram Bot Best Practices](https://core.telegram.org/bots/tutorial)

---

## 🔄 Versiya Tarixi

### v1.0.0 (2025-01-15)
- ✅ Asosiy funksiyalar
- ✅ Kanal boshqaruvi
- ✅ Xabar yuborish
- ✅ Admin paneli

### v1.1.0 (Rejada)
- 🔜 Rejali xabarlar
- 🔜 Statistika grafiklari
- 🔜 Ko'p tillilik
- 🔜 Webhook qo'llab-quvvatlash

---

**⭐️ Agar bot yoqsa, GitHub'da star qoldiring!**

Made with ❤️ by [Sizning Ismingiz]
