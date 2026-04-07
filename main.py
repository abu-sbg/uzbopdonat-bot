import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

# ТВОИ ДАННЫЕ
ADMIN_ID = 8414927732
SELLER_USERNAME = "@GGDONAT1"

# РЕКВИЗИТЫ ОПЛАТЫ
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

📸 После оплаты отправьте сюда чек / скрин оплаты
"""

# ТОВАРЫ
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
    "⭐ Telegram Premium": {
        "На 1 месяц": "60 000 сум",
        "На 1 год (каждый месяц по 40 000 сум)": "480 000 сум",
    }
}

# ОПИСАНИЯ
CATEGORY_INFO = {
    "⭐ Telegram Stars": """⭐ TELEGRAM STARS — ВЫГОДНО И БЫСТРО ⭐

🚀 Пополняй звёзды без лишних переплат
🔒 Надёжно | Проверено

💰 Цены:
• 100 ⭐ — 30 000 сум
• 150 ⭐ — 45 000 сум
• 250 ⭐ — 70 000 сум
• 350 ⭐ — 95 000 сум
• 500 ⭐ — 140 000 сум
• 750 ⭐ — 199 000 сум
• 1000 ⭐ — 285 000 сум

🔥 Успей купить по текущим ценам""",

    "💎 FC Points": """💎 FC POINTS — ЗАЛЕТАЙ ПО ВЫГОДЕ 💎

🚀 Хочешь топ состав и быстрый апгрейд?
Не трать время — бери FC Points с бонусом x2!

🔥 Только сейчас:
✔️ Двойной бонус к каждому паку
✔️ Моментальная выдача
✔️ Проверенный продавец

💰 Цены:
• 40 + 40 — 13 000 сум
• 100 + 100 — 25 000 сум
• 500 + 500 — 96 000 сум
• 1000 + 1000 — 195 000 сум
• 2000 + 2000 — 380 000 сум

⚡ Успей купить по этим ценам — потом будет дороже""",

    "🌟 Звёздный абонемент": """🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ 🌟

🔥 Легендарный 120 KLOSE уже доступен!
Прокачай состав и забери топ игрока прямо сейчас ⚽💥

💰 Цены:
⭐ Абонемент — 195 000 сум
🚀 +20 уровней — 370 000 сум

✨ Что получаешь:
✔️ Топовый игрок 120 OVR
✔️ Кучу наград и ресурсов
✔️ Быстрый прогресс
✔️ Максимум буста для аккаунта

⚡ Быстро | Надёжно | Безопасно""",

    "🔥 Brawl Pass": """🔥 BRAWL PASS АКЦИЯ 🔥

Прокачай свой аккаунт в Brawl Stars на максимум 🚀

💰 Цены:
🎟️ Brawl Pass — 70 000 сум
🎟️ Brawl Pass Plus — 110 000 сум

✨ Что получаешь:
✔️ Эксклюзивные награды
✔️ Быстрый прогресс
✔️ Больше ресурсов и ключей
✔️ Дополнительные бонусы в Plus

⚡ Быстро | Надёжно | Безопасно""",

    "💎 Гемы": """💎 ГЕМЫ В НАЛИЧИИ 💎

🚀 Быстрое пополнение | Надёжно | Без лишних заморочек

💰 Цены:
🔹 30 гемов — 16 000 сум
🔹 80 гемов — 40 000 сум
🔹 170 гемов — 74 000 сум
🔹 360 гемов — 145 000 сум
🔹 950 гемов — 355 000 сум
🔹 2000 гемов — 685 000 сум

✨ Почему мы?
✔️ Моментальная выдача
✔️ Выгодные цены
✔️ Проверенный сервис""",

    "⭐ Telegram Premium": """⭐ TELEGRAM PREMIUM ⭐

🚀 Открой больше возможностей в Telegram!
Эксклюзивные функции, высокая скорость и максимум комфорта 💎

💰 Тарифы:
📅 На 1 месяц — 60 000 сум
📆 На 1 год — 480 000 сум
(40 000 сум каждый месяц)

✨ Что получаешь:
✔️ Быстрая загрузка файлов
✔️ Увеличенные лимиты
✔️ Уникальные стикеры и реакции
✔️ Отключение рекламы
✔️ И многое другое!

⚡ Быстро | Надёжно | Доступно"""
}

# ПАМЯТЬ ЗАКАЗА
user_state = {}

# ГЛАВНОЕ МЕНЮ
main_keyboard = ReplyKeyboardMarkup(
    [
        ["🛍 Каталог", "💳 Оплата"],
        ["📞 Связь с продавцом", "📌 Как купить"],
        ["⭐ Отзывы", "ℹ️ О нас"]
    ],
    resize_keyboard=True
)

# КАТАЛОГ
catalog_keyboard = ReplyKeyboardMarkup(
    [
        ["⭐ Telegram Stars", "💎 FC Points"],
        ["🌟 Звёздный абонемент", "🔥 Brawl Pass"],
        ["💎 Гемы", "⭐ Telegram Premium"],
        ["⬅️ Назад"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = {}
    await update.message.reply_text(
        "👋 Добро пожаловать в магазин доната!\n\nВыберите нужный раздел:",
        reply_markup=main_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_state:
        user_state[user_id] = {}

    # Главное меню
    if text == "🛍 Каталог":
        await update.message.reply_text("📦 Выберите категорию:", reply_markup=catalog_keyboard)
        return

    if text == "💳 Оплата":
        await update.message.reply_text(PAYMENT_TEXT, reply_markup=main_keyboard)
        return

    if text == "📞 Связь с продавцом":
        await update.message.reply_text(f"📩 Напишите продавцу: {SELLER_USERNAME}", reply_markup=main_keyboard)
        return

    if text == "📌 Как купить":
        await update.message.reply_text(
            "📌 Как купить:\n\n"
            "1. Выбери товар\n"
            "2. Посмотри цену\n"
            "3. Нажми «💳 Оплата»\n"
            "4. Оплати на карту\n"
            "5. Отправь сюда чек / скрин оплаты\n"
            "6. После этого продавец свяжется с тобой",
            reply_markup=main_keyboard
        )
        return

    if text == "⭐ Отзывы":
        await update.message.reply_text(
            "⭐ Отзывы пока можно отправлять вручную.\n\n"
            f"Если хочешь, я потом добавлю тебе отдельный раздел с отзывами и фото.",
            reply_markup=main_keyboard
        )
        return

    if text == "ℹ️ О нас":
        await update.message.reply_text(
            "ℹ️ Мы продаём донат быстро, безопасно и по выгодным ценам.\n\n"
            "⚡ Моментальная обработка\n"
            "🔒 Надёжно\n"
            "💎 Выгодные цены",
            reply_markup=main_keyboard
        )
        return

    if text == "⬅️ Назад":
        user_state[user_id] = {}
        await update.message.reply_text("🏠 Главное меню", reply_markup=main_keyboard)
        return

    # Категории
    if text in SHOP_DATA:
        user_state[user_id]["category"] = text
        items = SHOP_DATA[text]

        item_buttons = [[item] for item in items.keys()]
        item_buttons.append(["💳 Оплата"])
        item_buttons.append(["⬅️ Назад"])

        item_keyboard = ReplyKeyboardMarkup(item_buttons, resize_keyboard=True)

        await update.message.reply_text(
            CATEGORY_INFO[text] + "\n\n👇 Выберите товар:",
            reply_markup=item_keyboard
        )
        return

    # Товары
    selected_category = user_state[user_id].get("category")
    if selected_category and text in SHOP_DATA[selected_category]:
        price = SHOP_DATA[selected_category][text]

        user_state[user_id]["item"] = text
        user_state[user_id]["price"] = price

        await update.message.reply_text(
            f"🛒 Вы выбрали:\n\n"
            f"📦 Товар: {text}\n"
            f"💰 Цена: {price}\n\n"
            f"👇 Теперь нажмите «💳 Оплата» и после перевода отправьте сюда чек / скрин оплаты.",
            reply_markup=main_keyboard
        )

        try:
            user = update.effective_user
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"📥 Новая заявка!\n\n"
                    f"👤 Пользователь: @{user.username if user.username else 'нет username'}\n"
                    f"🆔 ID: {user.id}\n"
                    f"📦 Категория: {selected_category}\n"
                    f"🛒 Товар: {text}\n"
                    f"💰 Цена: {price}"
                )
            )
        except Exception as e:
            print("Ошибка отправки админу:", e)

        return

    await update.message.reply_text(
        "❗ Я не понял команду. Нажми кнопку ниже.",
        reply_markup=main_keyboard
    )

# ПРИЁМ ФОТО / ЧЕКА
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    order_info = user_state.get(user_id, {})
    category = order_info.get("category", "Не выбрано")
    item = order_info.get("item", "Не выбрано")
    price = order_info.get("price", "Не выбрано")

    photo = update.message.photo[-1]

    caption = (
        f"📸 Новый чек об оплате\n\n"
        f"👤 Пользователь: @{user.username if user.username else 'нет username'}\n"
        f"🆔 ID: {user.id}\n"
        f"📦 Категория: {category}\n"
        f"🛒 Товар: {item}\n"
        f"💰 Цена: {price}"
    )

    try:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo.file_id,
            caption=caption
        )

        await update.message.reply_text(
            "✅ Чек получен!\n\n"
            "Продавец скоро проверит оплату и свяжется с вами.",
            reply_markup=main_keyboard
        )
    except Exception as e:
        print("Ошибка отправки фото админу:", e)
        await update.message.reply_text(
            "❌ Не удалось отправить чек администратору.\nПопробуйте ещё раз.",
            reply_markup=main_keyboard
        )

def main():
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
