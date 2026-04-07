import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# ЛОГИ
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# TOKEN
# =========================
TOKEN = os.getenv("BOT_TOKEN")

# =========================
# ТВОИ ДАННЫЕ
# =========================
ADMIN_ID = 8414927732
SELLER_USERNAME = "@GGDONAT1"
REVIEWS_LINK = "https://t.me/uzdinat2"

# =========================
# ОПЛАТА
# =========================
PAYMENT_TEXT = """
💳 ОПЛАТА

Номер карты 💳 Click
5614 6805 0423 5934

Номер карты 💳 Payme
5614 6805 0423 5934

👤 Получатель:
ARTIKOVA ZUXRA

📱 Номер телефона:
+998 93 597 27 47

🏧 Можно в банкомате

❌ На номер НЕ кидать
❌ Переводить только на карту

🛑 За ошибочный перевод не ручаюсь

📸 После оплаты отправьте сюда чек/скрин оплаты
"""

# =========================
# ТОВАРЫ
# =========================
SHOP_DATA = {
    "⭐ Telegram Stars": {
        "100 ⭐": "30 000 сум",
        "150 ⭐": "45 000 сум",
        "250 ⭐": "70 000 сум",
        "350 ⭐": "95 000 сум",
        "500 ⭐": "140 000 сум",
        "750 ⭐": "199 000 сум",
        "1000 ⭐": "285 000 сум",
    },

    "💎 Telegram Premium": {
        "3 месяца": "195 000 сум",
        "6 месяцев": "265 000 сум",
        "12 месяцев": "460 000 сум",
    },

    "💎 FC Points": {
        "40 + 40": "13 000 сум",
        "100 + 100": "25 000 сум",
        "500 + 500": "96 000 сум",
        "1000 + 1000": "195 000 сум",
        "2000 + 2000": "380 000 сум",
    },

    "🌟 Звёздный абонемент": {
        "Абонемент": "195 000 сум",
        "+20 уровней": "370 000 сум",
    },

    "🔥 Brawl Pass": {
        "Brawl Pass": "70 000 сум",
        "Brawl Pass Plus": "110 000 сум",
    },

    "💎 Gems": {
        "30 гемов": "16 000 сум",
        "80 гемов": "40 000 сум",
        "170 гемов": "74 000 сум",
        "360 гемов": "145 000 сум",
        "950 гемов": "355 000 сум",
        "2000 гемов": "685 000 сум",
    },
}

# =========================
# ОПИСАНИЯ
# =========================
CATEGORY_TEXTS = {
    "⭐ Telegram Stars": """
⭐ Telegram Stars

🚀 Пополняй звёзды без лишних переплат
🔒 Надёжно | Проверено

💰 Выбери нужное количество ниже 👇
""",

    "💎 Telegram Premium": f"""
⭐ Telegram Premium ⭐

🚀 Открой больше возможностей в Telegram
Быстрее, удобнее и намного круче 💎

💰 Тарифы:
📅 3 месяца — 195 000 сум
📆 6 месяцев — 265 000 сум
👑 12 месяцев — 460 000 сум

🔥 Что получаешь:
✔️ Быстрая загрузка
✔️ Красивые реакции и эмодзи
✔️ Больше лимитов
✔️ Premium возможности

📩 Хочешь купить?
Пиши мне: {SELLER_USERNAME} / через бота

📝 Канал отзывов:
{REVIEWS_LINK}
""",

    "💎 FC Points": """
💎 FC POINTS — ЗАЛЕТАЙ ПО ВЫГОДЕ 💎

🚀 Хочешь топ состав и быстрый апгрейд?
Не трать время — бери FC Points с бонусом x2!

🔥 Только сейчас:
✔️ Двойной бонус к каждому паку
✔️ Моментальная выдача
✔️ Проверенный продавец

💰 Выбери пакет ниже 👇
""",

    "🌟 Звёздный абонемент": """
🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ 🌟

🔥 Легендарный 120 KLOSE уже доступен!
Прокачай состав и забери топ игрока прямо сейчас ⚽💥

✨ Что получаешь:
✔️ Топовый игрок 120 OVR
✔️ Кучу наград и ресурсов
✔️ Быстрый прогресс
✔️ Максимум буста для аккаунта

💰 Выбери вариант ниже 👇
""",

    "🔥 Brawl Pass": """
🔥 BRAWL PASS АКЦИЯ 🔥

Прокачай свой аккаунт в Brawl Stars на максимум 🚀

✨ Что получаешь:
✔️ Эксклюзивные награды
✔️ Быстрый прогресс
✔️ Больше ресурсов и ключей
✔️ Дополнительные бонусы в Plus

💰 Выбери вариант ниже 👇
""",

    "💎 Gems": """
💎 ГЕМЫ В НАЛИЧИИ 💎

🚀 Быстрое пополнение | Надежно | Без лишних заморочек

✨ Почему мы?
✔️ Моментальная выдача
✔️ Выгодные цены
✔️ Проверенный сервис

💰 Выбери нужный пакет ниже 👇
"""
}

# =========================
# МЕНЮ
# =========================
MAIN_MENU = [
    ["⭐ Telegram Stars", "💎 Telegram Premium"],
    ["💎 FC Points", "🌟 Звёздный абонемент"],
    ["🔥 Brawl Pass", "💎 Gems"],
    ["💳 Оплата", "🛠 Тех поддержка"],
    ["📝 Отзывы"]
]

def get_main_keyboard():
    return ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)

def get_category_keyboard(category_name):
    buttons = []

    for item, price in SHOP_DATA[category_name].items():
        buttons.append([f"{item} — {price}"])

    buttons.append(["📝 Отзывы"])
    buttons.append(["🔙 Назад в меню"])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
👋 Добро пожаловать в магазин доната!

🔥 Здесь можно купить:
⭐ Telegram Stars
💎 Telegram Premium
💎 FC Points
🌟 Звёздный абонемент
🔥 Brawl Pass
💎 Gems

⚡ Быстро | Надежно | Удобно

👇 Выберите нужный раздел ниже:
"""
    await update.message.reply_text(text, reply_markup=get_main_keyboard())

# =========================
# ОБРАБОТКА ТЕКСТА
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Если нажали категорию
    if text in SHOP_DATA:
        await update.message.reply_text(
            CATEGORY_TEXTS.get(text, "Выберите товар 👇"),
            reply_markup=get_category_keyboard(text)
        )
        return

    # Назад
    if text == "🔙 Назад в меню":
        await update.message.reply_text(
            "🔙 Вы вернулись в главное меню",
            reply_markup=get_main_keyboard()
        )
        return

    # Оплата
    if text == "💳 Оплата":
        await update.message.reply_text(
            PAYMENT_TEXT,
            reply_markup=get_main_keyboard()
        )
        return

    # Тех поддержка
    if text == "🛠 Тех поддержка":
        await update.message.reply_text(
            f"🛠 Тех поддержка:\n{SELLER_USERNAME}",
            reply_markup=get_main_keyboard()
        )
        return

    # Отзывы
    if text == "📝 Отзывы":
        await update.message.reply_text(
            f"📝 Канал отзывов:\n{REVIEWS_LINK}",
            reply_markup=get_main_keyboard()
        )
        return

    # Проверка выбранного товара
    selected = None
    selected_category = None

    for category, items in SHOP_DATA.items():
        for item, price in items.items():
            if text == f"{item} — {price}":
                selected = f"{item} — {price}"
                selected_category = category
                break
        if selected:
            break

    if selected:
        context.user_data["selected_product"] = selected
        context.user_data["selected_category"] = selected_category

        await update.message.reply_text(
            f"✅ Вы выбрали:\n\n📦 {selected_category}\n🛒 {selected}\n\nТеперь оплатите 👇"
        )
        await update.message.reply_text(PAYMENT_TEXT)
        return

    await update.message.reply_text(
        "❗ Пожалуйста, выберите кнопку из меню",
        reply_markup=get_main_keyboard()
    )

# =========================
# ФОТО ЧЕКОВ
# =========================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    selected_product = context.user_data.get("selected_product", "Не выбран")
    selected_category = context.user_data.get("selected_category", "Не выбрана")

    caption = f"""
🧾 НОВАЯ ОПЛАТА

👤 Покупатель: @{user.username if user.username else "нет username"}
🆔 ID: {user.id}
📦 Категория: {selected_category}
🛒 Товар: {selected_product}
"""

    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption
    )

    await update.message.reply_text(
        "✅ Чек отправлен продавцу!\n\n⏳ Ожидайте подтверждения.",
        reply_markup=get_main_keyboard()
    )

# =========================
# ДОКУМЕНТЫ / ФАЙЛЫ
# =========================
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    selected_product = context.user_data.get("selected_product", "Не выбран")
    selected_category = context.user_data.get("selected_category", "Не выбрана")

    caption = f"""
🧾 НОВАЯ ОПЛАТА (ФАЙЛ)

👤 Покупатель: @{user.username if user.username else "нет username"}
🆔 ID: {user.id}
📦 Категория: {selected_category}
🛒 Товар: {selected_product}
"""

    document = update.message.document.file_id

    await context.bot.send_document(
        chat_id=ADMIN_ID,
        document=document,
        caption=caption
    )

    await update.message.reply_text(
        "✅ Файл с оплатой отправлен продавцу!\n\n⏳ Ожидайте подтверждения.",
        reply_markup=get_main_keyboard()
    )

# =========================
# MAIN
# =========================
def main():
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
