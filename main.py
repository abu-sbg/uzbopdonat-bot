import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# -------------------- ЛОГИ --------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# -------------------- ТОКЕН --------------------
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден!")

# -------------------- ТВОИ ДАННЫЕ --------------------
ADMIN_ID = 8414927732
SELLER_USERNAME = "@GGDONAT1"
REVIEWS_CHANNEL = "https://t.me/uzdinat2"

# -------------------- ОПЛАТА --------------------
PAYMENT_TEXT = """
💳 *ОПЛАТА*

💳 *Номер карты Click:*
`5614680504235934`

💳 *Номер карты Payme:*
`5614680504235934`

👤 *Получатель:*
ARTIKOVA ZUXRA

📱 *Номер телефона:*
`+998 93 597 27 47`

🏧 *Можно в банкомате*

❌ *На номер не кидать*
❌ *Переводить только на карту*

🛑 *За ошибочный перевод не ручаюсь*

📸 *После оплаты отправьте сюда чек / скрин оплаты*
"""

# -------------------- ОТЗЫВЫ --------------------
REVIEWS_TEXT = f"""
⭐ *ОТЗЫВЫ КЛИЕНТОВ* ⭐

Спасибо всем за доверие ❤️

📢 *Канал с отзывами:*
{REVIEWS_CHANNEL}

👇 Нажми кнопку ниже, чтобы открыть отзывы.
"""

# -------------------- ТОВАРЫ --------------------
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
    "💎 Гемы": {
        "30 гемов": "16 000 сум",
        "80 гемов": "40 000 сум",
        "170 гемов": "74 000 сум",
        "360 гемов": "145 000 сум",
        "950 гемов": "355 000 сум",
        "2000 гемов": "685 000 сум",
    },
    "⭐ Telegram Premium ⭐": {
        "📅 На 1 месяц — 60 000 сум": "60 000 сум",
        "📆 На 1 год — 480 000 сум": "480 000 сум",
    }
}

CATEGORY_INFO = {
    "⭐ Telegram Stars": """⭐ *TELEGRAM STARS — ВЫГОДНО И БЫСТРО* ⭐

🚀 Пополняй звёзды без лишних переплат
🔒 Надёжно | Проверено

💰 *Цены:*
• 100 ⭐ — 30 000 сум
• 150 ⭐ — 45 000 сум
• 250 ⭐ — 70 000 сум
• 350 ⭐ — 95 000 сум
• 500 ⭐ — 140 000 сум
• 750 ⭐ — 199 000 сум
• 1000 ⭐ — 285 000 сум

🔥 Успей купить по текущим ценам
""",

    "💎 FC Points": """💎 *FC POINTS — ЗАЛЕТАЙ ПО ВЫГОДЕ* 💎

🚀 Хочешь топ состав и быстрый апгрейд?
Не трать время — бери FC Points с бонусом x2!

🔥 *Только сейчас:*
✔️ Двойной бонус к каждому паку
✔️ Моментальная выдача
✔️ Проверенный продавец

💰 *Цены:*
• 40 + 40 — 13 000 сум
• 100 + 100 — 25 000 сум
• 500 + 500 — 96 000 сум
• 1000 + 1000 — 195 000 сум
• 2000 + 2000 — 380 000 сум
""",

    "🌟 Звёздный абонемент": """🌟 *ЗВЁЗДНЫЙ АБОНЕМЕНТ* 🌟

🔥 Легендарный 120 KLOSE уже доступен!
Прокачай состав и забери топ игрока прямо сейчас ⚽💥

💰 *Цены:*
⭐ Абонемент — 195 000 сум
🚀 +20 уровней — 370 000 сум

✨ *Что получаешь:*
✔️ Топовый игрок 120 OVR
✔️ Кучу наград и ресурсов
✔️ Быстрый прогресс
✔️ Максимум буста для аккаунта
""",

    "🔥 Brawl Pass": """🔥 *BRAWL PASS АКЦИЯ* 🔥

Прокачай свой аккаунт в Brawl Stars на максимум 🚀

💰 *Цены:*
🎟️ Brawl Pass — 70 000 сум
🎟️ Brawl Pass Plus — 110 000 сум

✨ *Что получаешь:*
✔️ Эксклюзивные награды
✔️ Быстрый прогресс
✔️ Больше ресурсов и ключей
✔️ Дополнительные бонусы в Plus
""",

    "💎 Гемы": """💎 *ГЕМЫ В НАЛИЧИИ* 💎

🚀 Быстрое пополнение | Надёжно | Без лишних заморочек

💰 *Цены:*
🔹 30 гемов — 16 000 сум
🔹 80 гемов — 40 000 сум
🔹 170 гемов — 74 000 сум
🔹 360 гемов — 145 000 сум
🔹 950 гемов — 355 000 сум
🔹 2000 гемов — 685 000 сум
""",

    "⭐ Telegram Premium ⭐": """⭐ *TELEGRAM PREMIUM* ⭐

🚀 Открой больше возможностей в Telegram!
Эксклюзивные функции, высокая скорость и максимум комфорта 💎

💰 *Тарифы:*
📅 На 1 месяц — 60 000 сум
📆 На год — всего 40 000 сум / месяц (выгоднее 🔥)

✨ *Что получаешь:*
✔️ Быстрая загрузка файлов
✔️ Увеличенные лимиты
✔️ Уникальные стикеры и реакции
✔️ Отключение рекламы
✔️ И многое другое!

📩 *Заказать:* @GGDONAT1
⚡ Быстро | Надёжно | Доступно

Не упусти шанс прокачать свой Telegram 💜
"""
}

# -------------------- КЛАВИАТУРЫ --------------------
def main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🛍 Каталог")],
            [KeyboardButton("💳 Оплата"), KeyboardButton("⭐ Отзывы")],
            [KeyboardButton("📞 Связь")]
        ],
        resize_keyboard=True
    )

def catalog_keyboard():
    keyboard = []
    for category in SHOP_DATA.keys():
        keyboard.append([InlineKeyboardButton(category, callback_data=f"cat|{category}")])
    return InlineKeyboardMarkup(keyboard)

def products_keyboard(category):
    keyboard = []
    for product in SHOP_DATA[category].keys():
        keyboard.append([InlineKeyboardButton(product, callback_data=f"buy|{category}|{product}")])
    keyboard.append([InlineKeyboardButton("⬅ Назад", callback_data="back_catalog")])
    return InlineKeyboardMarkup(keyboard)

def reviews_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Открыть канал отзывов", url=REVIEWS_CHANNEL)]
    ])

# -------------------- /start --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"""👋 Привет, {user.first_name}!

Добро пожаловать в магазин доната 🎮

Здесь ты можешь купить:
⭐ Telegram Stars
💎 FC Points
🌟 Звёздный абонемент
🔥 Brawl Pass
💎 Гемы
⭐ Telegram Premium

👇 Выбери нужный раздел:
"""
    await update.message.reply_text(text, reply_markup=main_menu())

# -------------------- ОБРАБОТКА ТЕКСТА --------------------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🛍 Каталог":
        await update.message.reply_text("📦 Выбери категорию:", reply_markup=catalog_keyboard())

    elif text == "💳 Оплата":
        await update.message.reply_text(PAYMENT_TEXT, parse_mode="Markdown")

    elif text == "⭐ Отзывы":
        await update.message.reply_text(
            REVIEWS_TEXT,
            parse_mode="Markdown",
            reply_markup=reviews_keyboard()
        )

    elif text == "📞 Связь":
        await update.message.reply_text(
            f"📩 Продавец: {SELLER_USERNAME}\n🆔 ID: `{ADMIN_ID}`",
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text("Выбери кнопку ниже 👇", reply_markup=main_menu())

# -------------------- INLINE КНОПКИ --------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "back_catalog":
        await query.message.reply_text("📦 Выбери категорию:", reply_markup=catalog_keyboard())
        return

    if data.startswith("cat|"):
        category = data.split("|", 1)[1]
        text = CATEGORY_INFO.get(category, f"📦 {category}")
        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=products_keyboard(category)
        )

    elif data.startswith("buy|"):
        _, category, product = data.split("|", 2)
        price = SHOP_DATA[category][product]

        context.user_data["selected_category"] = category
        context.user_data["selected_product"] = product
        context.user_data["selected_price"] = price

        text = f"""🛒 *Ваш заказ:*

📦 *Категория:* {category}
🎁 *Товар:* {product}
💰 *Цена:* {price}

{PAYMENT_TEXT}
"""
        await query.message.reply_text(text, parse_mode="Markdown")

# -------------------- ФОТО ОПЛАТЫ --------------------
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]

    category = context.user_data.get("selected_category", "Не выбрано")
    product = context.user_data.get("selected_product", "Не выбрано")
    price = context.user_data.get("selected_price", "Не выбрано")

    caption = f"""💸 *Новая оплата!*

👤 *Имя:* {user.first_name}
🆔 *ID:* `{user.id}`
🔗 *Username:* @{user.username if user.username else 'нет username'}

📦 *Категория:* {category}
🎁 *Товар:* {product}
💰 *Цена:* {price}
"""

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=caption,
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "✅ Скрин оплаты отправлен продавцу!\n\n⏳ Ожидайте подтверждения.",
        reply_markup=main_menu()
    )

# -------------------- ЗАПУСК --------------------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
