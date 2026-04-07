import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)

# =========================
# НАСТРОЙКИ
# =========================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Добавь его в Railway Variables")

ADMIN_ID = 8414927732
SELLER_USERNAME = "@GGDONAT1"
REVIEWS_LINK = "https://t.me/uzdinat2"

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

❌ На номер не кидать
❌ Переводить только на карту

🛑 За ошибочный перевод не ручаюсь

📸 После оплаты отправьте сюда чек / скрин оплаты
"""

# =========================
# ТОВАРЫ
# =========================

SHOP_DATA = {
    "⭐ Звёзды Telegram": {
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

    "💎 Гемы": {
        "30 гемов": "16 000 сум",
        "80 гемов": "40 000 сум",
        "170 гемов": "74 000 сум",
        "360 гемов": "145 000 сум",
        "950 гемов": "355 000 сум",
        "2000 гемов": "685 000 сум",
    },

    "🔥 Brawl Pass": {
        "Brawl Pass": "70 000 сум",
        "Brawl Pass Plus": "110 000 сум",
    },

    "🌟 Звёздный абонемент": {
        "Абонемент": "195 000 сум",
        "+20 уровней": "370 000 сум",
    },

    "⚽ FC Points": {
        "40 + 40": "13 000 сум",
        "100 + 100": "25 000 сум",
        "500 + 500": "96 000 сум",
        "1000 + 1000": "195 000 сум",
        "2000 + 2000": "380 000 сум",
    }
}

CATEGORY_TEXTS = {
    "⭐ Звёзды Telegram": """
⭐ TELEGRAM STARS — ВЫГОДНО И БЫСТРО ⭐

🚀 Пополняй звёзды без лишних переплат
🔒 Надёжно | Проверено

💰 Выбери нужное количество ниже 👇
""",

    "💎 Telegram Premium": """
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
Пиши мне: @GGDONAT1 / через бота: @uzbtopdonat_bot
""",

    "💎 Гемы": """
💎 ГЕМЫ В НАЛИЧИИ 💎

🚀 Быстрое пополнение | Надёжно | Без лишних заморочек

💰 Выбери нужный пак ниже 👇
""",

    "🔥 Brawl Pass": """
🔥 BRAWL PASS АКЦИЯ 🔥

Прокачай свой аккаунт в Brawl Stars на максимум 🚀

🎟️ Выбери вариант ниже 👇
""",

    "🌟 Звёздный абонемент": """
🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ 🌟

🔥 Легендарный 120 KLOSE уже доступен!
Прокачай состав и забери топ игрока прямо сейчас ⚽💥

⭐ Выбери вариант ниже 👇
""",

    "⚽ FC Points": """
💎 FC POINTS — ЗАЛЕТАЙ ПО ВЫГОДЕ 💎

🚀 Хочешь топ состав и быстрый апгрейд?
Не трать время — бери FC Points с бонусом x2!

⚡ Выбери нужный пак ниже 👇
"""
}

# =========================
# ЛОГИ
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# КНОПКИ
# =========================

main_keyboard = ReplyKeyboardMarkup(
    [
        ["⭐ Звёзды Telegram", "💎 Telegram Premium"],
        ["💎 Гемы", "🔥 Brawl Pass"],
        ["🌟 Звёздный абонемент", "⚽ FC Points"],
        ["📝 Отзывы", "📞 Связаться с продавцом"],
        ["💳 Оплата"],
    ],
    resize_keyboard=True
)

def get_reviews_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Открыть отзывы", url=REVIEWS_LINK)]
    ])

def get_seller_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 Написать продавцу", url=f"https://t.me/{SELLER_USERNAME.replace('@', '')}")]
    ])

def build_product_buttons(category_name):
    keyboard = []

    for item_name, price in SHOP_DATA[category_name].items():
        callback_data = f"buy|{category_name}|{item_name}|{price}"
        keyboard.append([
            InlineKeyboardButton(f"{item_name} — {price}", callback_data=callback_data)
        ])

    keyboard.append([InlineKeyboardButton("📝 Отзывы", url=REVIEWS_LINK)])
    keyboard.append([InlineKeyboardButton("📩 Написать продавцу", url=f"https://t.me/{SELLER_USERNAME.replace('@', '')}")])

    return InlineKeyboardMarkup(keyboard)

# =========================
# СТАРТ
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
👋 Добро пожаловать!

Здесь можно купить:

⭐ Telegram Stars
💎 Telegram Premium
💎 Гемы
🔥 Brawl Pass
🌟 Звёздный абонемент
⚽ FC Points

⚡ Быстро | Надёжно | Удобно

📩 Продавец: {SELLER_USERNAME}
📝 Отзывы: {REVIEWS_LINK}

Выберите нужный раздел ниже 👇
"""
    await update.message.reply_text(text, reply_markup=main_keyboard)

# =========================
# МЕНЮ
# =========================

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in SHOP_DATA:
        category_text = CATEGORY_TEXTS.get(text, f"📦 {text}")
        await update.message.reply_text(
            category_text,
            reply_markup=build_product_buttons(text)
        )

    elif text == "📝 Отзывы":
        await update.message.reply_text(
            f"📝 Отзывы клиентов:\n{REVIEWS_LINK}",
            reply_markup=get_reviews_button()
        )

    elif text == "📞 Связаться с продавцом":
        await update.message.reply_text(
            f"📩 Продавец: {SELLER_USERNAME}\n🆔 ID: {ADMIN_ID}",
            reply_markup=get_seller_button()
        )

    elif text == "💳 Оплата":
        await update.message.reply_text(PAYMENT_TEXT)

    else:
        await update.message.reply_text(
            "Выбери нужную кнопку ниже 👇",
            reply_markup=main_keyboard
        )

# =========================
# ПОКУПКА
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("buy|"):
        try:
            _, category, item_name, price = data.split("|", 3)
        except ValueError:
            await query.message.reply_text("❌ Ошибка товара.")
            return

        context.user_data["selected_category"] = category
        context.user_data["selected_item"] = item_name
        context.user_data["selected_price"] = price

        order_text = f"""
🛒 ВАШ ЗАКАЗ

📦 Категория: {category}
🎁 Товар: {item_name}
💰 Цена: {price}

{PAYMENT_TEXT}
"""

        await query.message.reply_text(order_text)

        user = query.from_user
        admin_text = f"""
📥 НОВАЯ ЗАЯВКА

👤 Пользователь: @{user.username if user.username else "без username"}
🆔 ID: {user.id}
📛 Имя: {user.first_name}

📦 Категория: {category}
🎁 Товар: {item_name}
💰 Цена: {price}
"""

        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)

# =========================
# ФОТО / ЧЕКИ
# =========================

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    category = context.user_data.get("selected_category", "Не выбрано")
    item_name = context.user_data.get("selected_item", "Не выбрано")
    price = context.user_data.get("selected_price", "Не выбрано")

    caption = f"""
💸 НОВЫЙ ЧЕК ОБ ОПЛАТЕ

👤 Пользователь: @{user.username if user.username else "без username"}
🆔 ID: {user.id}
📛 Имя: {user.first_name}

📦 Категория: {category}
🎁 Товар: {item_name}
💰 Цена: {price}
"""

    photo = update.message.photo[-1]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=caption
    )

    await update.message.reply_text(
        "✅ Чек отправлен продавцу!\n\n⏳ Ожидайте подтверждения.",
        reply_markup=main_keyboard
    )

# =========================
# ДОКУМЕНТ / ФАЙЛ ЧЕКА
# =========================

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    category = context.user_data.get("selected_category", "Не выбрано")
    item_name = context.user_data.get("selected_item", "Не выбрано")
    price = context.user_data.get("selected_price", "Не выбрано")

    caption = f"""
📄 НОВЫЙ ФАЙЛ / ЧЕК

👤 Пользователь: @{user.username if user.username else "без username"}
🆔 ID: {user.id}
📛 Имя: {user.first_name}

📦 Категория: {category}
🎁 Товар: {item_name}
💰 Цена: {price}
"""

    document = update.message.document

    await context.bot.send_document(
        chat_id=ADMIN_ID,
        document=document.file_id,
        caption=caption
    )

    await update.message.reply_text(
        "✅ Файл/чек отправлен продавцу!\n\n⏳ Ожидайте подтверждения.",
        reply_markup=main_keyboard
    )

# =========================
# ТЕКСТ ПОСЛЕ ОПЛАТЫ
# =========================

async def forward_text_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # чтобы меню не пересылалось как заказ
    if text in SHOP_DATA or text in ["📝 Отзывы", "📞 Связаться с продавцом", "💳 Оплата"]:
        return

    user = update.effective_user

    category = context.user_data.get("selected_category", "Не выбрано")
    item_name = context.user_data.get("selected_item", "Не выбрано")
    price = context.user_data.get("selected_price", "Не выбрано")

    admin_text = f"""
💬 НОВОЕ СООБЩЕНИЕ ОТ КЛИЕНТА

👤 Пользователь: @{user.username if user.username else "без username"}
🆔 ID: {user.id}
📛 Имя: {user.first_name}

📦 Категория: {category}
🎁 Товар: {item_name}
💰 Цена: {price}

📝 Сообщение:
{text}
"""

    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)

    await update.message.reply_text(
        "✅ Сообщение отправлено продавцу.",
        reply_markup=main_keyboard
    )

# =========================
# ЗАПУСК
# =========================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_text_to_admin))

    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
