import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
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
# ТЕКСТ ОПЛАТЫ
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
    "⭐ Звезды Telegram": {
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

    "⚽ FC Points": {
        "FC Points 1": "Цена уточняется",
        "FC Points 2": "Цена уточняется",
        "FC Points 3": "Цена уточняется",
    },

    "🔥 Brawl Pass": {
        "Brawl Pass": "Цена уточняется",
        "Brawl Pass Plus": "Цена уточняется",
    },

    "💠 Gems": {
        "Пакет 1": "Цена уточняется",
        "Пакет 2": "Цена уточняется",
        "Пакет 3": "Цена уточняется",
    },

    "🎫 Абик": {
        "Абик 1": "Цена уточняется",
        "Абик 2": "Цена уточняется",
    },
}

# =========================
# КНОПКИ
# =========================
MAIN_MENU = [
    ["⭐ Звезды Telegram", "💎 Telegram Premium"],
    ["⚽ FC Points", "🔥 Brawl Pass"],
    ["💠 Gems", "🎫 Абик"],
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
    text = f"""
👋 Добро пожаловать в магазин доната!

🔥 Здесь можно купить:
⭐ Telegram Stars
💎 Telegram Premium
⚽ FC Points
🔥 Brawl Pass
💠 Gems
🎫 Абик

⚡ Быстро | Надежно | Удобно

👇 Выберите нужный раздел ниже:
"""
    await update.message.reply_text(text, reply_markup=get_main_keyboard())

# =========================
# ОБРАБОТКА ТЕКСТА
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Главное меню
    if text in SHOP_DATA:
        category_texts = {
            "⭐ Звезды Telegram": """
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
📅 3 месяца — 195.000 сум
📆 6 месяцев — 265.000 сум
👑 12 месяцев — 460.000 сум

🔥 Что получаешь:
✔️ Быстрая загрузка
✔️ Красивые реакции и эмодзи
✔️ Больше лимитов
✔️ Premium возможности

📩 Хочешь купить?
Пиши мне: {SELLER_USERNAME} / через бота

Канал отзывов:
{REVIEWS_LINK}
""",
            "⚽ FC Points": """
⚽ FC Points

🔥 Выберите нужный вариант ниже 👇
""",
            "🔥 Brawl Pass": """
🔥 Brawl Pass

🎮 Выберите нужный вариант ниже 👇
""",
            "💠 Gems": """
💠 Gems

💎 Выберите нужный пакет ниже 👇
""",
            "🎫 Абик": """
🎫 Абик

📦 Выберите нужный вариант ниже 👇
"""
        }

        await update.message.reply_text(
            category_texts.get(text, "Выберите товар 👇"),
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
        await update.message.reply_text(PAYMENT_TEXT, reply_markup=get_main_keyboard())
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

    # Если выбрали конкретный товар
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
            f"✅ Вы выбрали:\n\n{selected_category}\n{selected}\n\nТеперь оплатите 👇"
        )
        await update.message.reply_text(PAYMENT_TEXT)
        return

    # Если текст непонятен
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
# ДОКУМЕНТЫ/ФАЙЛЫ ЧЕКОВ
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
