from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7755831899:AAHa_dY3xNH0jv1Hn0yUVN4FFmUxFB3WQkw"

catalog = {
    "Натуральное мыло": [
        {
            "name": "Календула и облепиха",
            "price": "450₽",
            "desc": "Мыло с натуральным маслом облепихи для смягчения кожи. Подходит для лица и тела.",
            "image": "IMG_8981.png"
        },
        {
            "name": "Глинтвейн",
            "price": "450₽",
            "desc": "Мыло с ярким ароматом корицы и эфирным маслом апельсина для нежного очищения кожи. Подходит для лица и тела.",
            "image": "IMG_8980.png"
        },
        {
            "name": "Манго и апельсин",
            "price": "450₽",
            "desc": "Мыло с органическим маслом манго и эфирным маслом апельсина. Бережно очищает и увлажняет кожу. Подходит для лица и тела.",
            "image": "IMG_8979.png"
        },
        {
            "name": "Роза и шелк",
            "price": "450₽",
            "desc": "Натуральное мыло с эфирным маслом розы, гидролатом розы и шелком. Подходит для чувствительной кожи, смягчает и увлажняет.",
            "image": "IMG_8978.png"
        }
    ],
    "Гидролаты": [
        {
            "name": "Гидролат малины",
            "price": "400₽",
            "desc": "Гидролат малины обладает свойством увлажнять и успокаивать кожу; обладает очищающим и тонизирующим действием.",
            "image": None
        },
        {
            "name": "Гидролат черной смородины",
            "price": "400₽",
            "desc": "Гидролат чёрной смородины помогает замедлять процессы старения, выравнивает тон кожи. Применяется для восстановления сухой и раздражённой кожи.",
            "image": None
        }
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"category|{cat}")]
                for cat in catalog]
    await update.message.reply_text("🌿 Добро пожаловать в каталог MOZ cosmetics!\n\nВыберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split('|')

    if data[0] == "category":
        category = data[1]
        keyboard = [[InlineKeyboardButton(p["name"], callback_data=f"product|{category}|{i}")]
                    for i, p in enumerate(catalog[category])]
        keyboard.append([
            InlineKeyboardButton("🏠 Главная", callback_data="back_to_main")
        ])
        try:
            await query.edit_message_text(
                text=f"Категория: {category}\nВыберите продукт:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"Категория: {category}\nВыберите продукт:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    elif data[0] == "product":
        category = data[1]
        index = int(data[2])
        product = catalog[category][index]
        caption = f"<b>{product['name']}</b>\nЦена: {product['price']}\n\n{product['desc']}"
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔙 Назад", callback_data=f"category|{category}"),
                InlineKeyboardButton("🏠 Главная", callback_data="back_to_main")
            ]
        ])
        try:
            await query.message.delete()
        except:
            pass
        if product["image"]:
            try:
                with open(product["image"], 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=query.message.chat_id,
                        photo=photo,
                        caption=caption,
                        parse_mode="HTML",
                        reply_markup=buttons
                    )
            except:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="⚠️ Не удалось загрузить изображение.",
                    reply_markup=buttons
                )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=caption,
                parse_mode="HTML",
                reply_markup=buttons
            )

    elif data[0] == "back_to_main":
        keyboard = [[InlineKeyboardButton(cat, callback_data=f"category|{cat}")]
                    for cat in catalog]
        try:
            await query.edit_message_text("🌿 Добро пожаловать в каталог MOZ cosmetics!\n\nВыберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            await context.bot.send_message(chat_id=query.message.chat_id, text="🌿 Добро пожаловать в каталог MOZ cosmetics!\n\nВыберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    print("Бот запущен!")
    app.run_polling()
