import telebot
from telebot import types
from collections import defaultdict

TOKEN = "8400828602:AAGmF8japcI3YkWRmvd2o9QXoohcYc4I7vQ"
bot = telebot.TeleBot(TOKEN)

ADMIN_USERNAME = "@thevladzio"

# Данные
user_spending = defaultdict(int)      # {user_id: сумма покупок (в т.ч. рефералов)}
referrals = defaultdict(list)         # {referrer_id: [user_id рефералов]}
user_referrer = {}                    # {user_id: referrer_id}
reviews = []                         # отзывы покупателей

user_language = {}                   # {user_id: "ru" или "ua"}
user_carts = defaultdict(list)      # {user_id: [(product_name, price), ...]}

texts = {
    "choose_lang": "🌍 Пожалуйста, выберите удобный язык / Будь ласка, оберіть зручну мову:",
    "lang_ru": "🇷🇺 Русский",
    "lang_ua": "🇺🇦 Українська",
    "welcome_ru": "💨 Добро пожаловать в *VapeAlva*!\nВыберите интересующий раздел:",
    "welcome_ua": "💨 Ласкаво просимо до *VapeAlva*!\nОберіть потрібний розділ:",
    "menu_catalog_ru": "📂 Каталог",
    "menu_catalog_ua": "📂 Каталог",
    "menu_order_ru": "🛒 Заказать",
    "menu_order_ua": "🛒 Замовити",
    "menu_cart_ru": "🛍 Корзина",
    "menu_cart_ua": "🛍 Кошик",
    "menu_about_ru": "ℹ️ О нас",
    "menu_about_ua": "ℹ️ Про нас",
    "menu_partner_ru": "🤝 Партнёрская программа",
    "menu_partner_ua": "🤝 Партнерська програма",
    "menu_orders_ru": "📦 Мои заказы",
    "menu_orders_ua": "📦 Мої замовлення",
    "menu_reviews_ru": "✍ Оставить отзыв",
    "menu_reviews_ua": "✍ Залишити відгук",
    "back_btn_ru": "⬅ Назад",
    "back_btn_ua": "⬅ Назад",
    "please_choose_ru": "Пожалуйста, выберите пункт меню.",
    "please_choose_ua": "Будь ласка, оберіть пункт меню.",
    "reviews_list_empty_ru": "Пока нет отзывов. Будьте первым!",
    "reviews_list_empty_ua": "Поки немає відгуків. Будьте першими!",
    "thank_review_ru": "✅ Спасибо! Ваш отзыв добавлен.",
    "thank_review_ua": "✅ Дякуємо! Ваш відгук додано.",
    "partner_program_ru": (
        "💼 *Партнёрская программа VapeAlva*\n\n"
        "Приглашайте друзей по вашей личной ссылке и получайте ценные бонусы!\n\n"
        "👥 Приглашено пользователей: *{count}*\n"
        "🎁 Когда ваши приглашённые суммарно совершат покупки на *4100 грн*, "
        "вы получите подарок на выбор:\n"
        "• 💨 Любая жидкость из нашего ассортимента\n"
        "• 🔄 Или два картриджа по вашему вкусу\n\n"
        "📌 Всё просто: отправляйте ссылку друзьям, они заказывают — вы копите бонусы.\n\n"
        "🔗 Ваша ссылка: {link}\n"
        "💰 Потрачено по вашей ссылке: {spent} грн"
    ),
    "partner_program_ua": (
        "💼 *Партнерська програма VapeAlva*\n\n"
        "Запрошуйте друзів за вашим унікальним посиланням і отримуйте цінні бонуси!\n\n"
        "👥 Запрошено користувачів: *{count}*\n"
        "🎁 Коли ваші запрошені зроблять покупки на суму *4100 грн*, "
        "ви отримаєте подарунок на вибір:\n"
        "• 💨 Будь-яка рідина з нашого асортименту\n"
        "• 🔄 Або два картриджі на ваш смак\n\n"
        "📌 Просто надсилайте посилання друзям, вони замовляють — ви накопичуєте бонуси.\n\n"
        "🔗 Ваше посилання: {link}\n"
        "💰 Витрачено по вашому посиланню: {spent} грн"
    ),
    "about_ru": (
        "💨 *VapeAlva* — магазин вейп-товаров с проверенными поставщиками.\n"
        "🚀 Доставка по всей Украине.\n\n"
        "📞 Поддержка: @helperAlva"
    ),
    "about_ua": (
        "💨 *VapeAlva* — магазин вейп-товарів з перевіреними постачальниками.\n"
        "🚀 Доставка по всій Україні.\n\n"
        "📞 Підтримка: @helperAlva"
    ),
    "cart_empty_ru": "🛒 Ваша корзина пуста.",
    "cart_empty_ua": "🛍 Ваш кошик порожній.",
    "cart_title_ru": "🛒 Ваша корзина:\n\n",
    "cart_title_ua": "🛍 Ваш кошик:\n\n",
    "cart_total_ru": "\n*Общая сумма:* {total} ₴",
    "cart_total_ua": "\n*Загальна сума:* {total} ₴",
    "order_button_ru": "Оформить заказ",
    "order_button_ua": "Оформити замовлення",
    "pay_method_ru": "Выберите способ оплаты:",
    "pay_method_ua": "Оберіть спосіб оплати:",
    "pay_on_delivery_ru": "Оплата при получении",
    "pay_on_delivery_ua": "Оплата при отриманні",
    "pay_prepay_ru": "Оплата Картой",
    "pay_prepay_ua": "Оплата Карткою",
    "pay_on_delivery_info_ru": "📞 С вами свяжется в ближайшее время наш менеджер для подтверждения заказа.",
    "pay_on_delivery_info_ua": "📞 З вами найближчим часом зв'яжеться наш менеджер для підтвердження замовлення.",
    "prepay_info_ru": (
        "💳 Оплата через бота:\n\n"
        "ФИО карты: Владислав. Г.\n"
        "Номер карты: `4441 1110 3909 5041`\n\n"
        "После оплаты нажмите кнопку ниже, чтобы подтвердить оплату."
    ),
    "prepay_info_ua": (
        "💳 Оплата через бота:\n\n"
        "ПІБ карти: Владислав. Г.\n"
        "Номер карти: `4441 1110 3909 5041`\n\n"
        "Після оплати натисніть кнопку нижче, щоб підтвердити оплату."
    ),
    "pay_done_ru": "Оплачено",
    "pay_done_ua": "Оплачено",
    "clear_cart_ru": "Очистить корзину",
    "clear_cart_ua": "Очистити кошик",
    "please_choose_ru": "Пожалуйста, выберите пункт меню.",
    "please_choose_ua": "Будь ласка, оберіть пункт меню.",
    "referral_purchase_ru": "💰 Ваш реферал {user} сделал покупку на сумму {amount} грн.\nОбщая сумма покупок по вашей ссылке: {total} грн.",
    "referral_purchase_ua": "💰 Ваш реферал {user} зробив покупку на суму {amount} грн.\nЗагальна сума покупок по вашому посиланню: {total} грн."
}

def t(key, lang="ru"):
    key_full = f"{key}_{lang}"
    return texts.get(key_full) or texts.get(key)

# --- Обработка языкового выбора ---

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) > 1:
        # Если пришла реферальная ссылка
        try:
            referrer_id = int(args[1])
            if referrer_id != user_id and user_id not in referrals[referrer_id]:
                referrals[referrer_id].append(user_id)
                user_referrer[user_id] = referrer_id
                try:
                    bot.send_message(referrer_id,
                                     f"🎉 Новый пользователь @{message.from_user.username or message.from_user.first_name} "
                                     f"зарегистрировался по вашей реферальной ссылке!")
                except Exception:
                    pass
        except Exception:
            pass
    if user_id not in user_language:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_ru = types.KeyboardButton(texts["lang_ru"])
        btn_ua = types.KeyboardButton(texts["lang_ua"])
        markup.add(btn_ru, btn_ua)
        bot.send_message(user_id, texts["choose_lang"], reply_markup=markup)
    else:
        send_main_menu(message)

@bot.message_handler(func=lambda m: m.text in [texts["lang_ru"], texts["lang_ua"]])
def set_language(message):
    user_id = message.from_user.id
    if message.text == texts["lang_ru"]:
        user_language[user_id] = "ru"
    else:
        user_language[user_id] = "ua"
    send_main_menu(message)

def send_main_menu(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(
        types.KeyboardButton(t("menu_order", lang)),
        types.KeyboardButton(t("menu_cart", lang)),
        types.KeyboardButton(t("menu_about", lang)),
        types.KeyboardButton(t("menu_partner", lang)),
        types.KeyboardButton(t("menu_orders", lang)),
        types.KeyboardButton(t("menu_reviews", lang)),
    )
    bot.send_message(user_id, t("welcome", lang), parse_mode="Markdown", reply_markup=markup)

# --- Основное меню ---

@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    text = message.text

    if text == t("menu_order", lang):
        show_catalog_menu(message)

    elif text == t("menu_cart", lang):
        show_cart(message)

    elif text == "💨 Под-системы" or text == "💨 Під-системи":
        bot.send_message(
            user_id,
            "Раздел с под-системами пока в разработке." if lang == "ru" else "Розділ із під-системами поки в розробці."
        )

    elif text == "🧃 Жидкости" or text == "🧃 Рідини":
        bot.send_message(
            user_id,
            "Раздел с жидкостями пока в разработке." if lang == "ru" else "Розділ з рідинами поки в розробці."
        )

    elif text == "🔄 Картриджи" or text == "🔄 Картриджі":
        show_cartridge_brands(message)

    elif text == "Vaporesso":
        show_vaporesso_pods(message)

    elif text == "Voopoo":
        if lang == "ru":
            bot.send_message(user_id, "Раздел Воопоо пока в разработке.")
        else:
            bot.send_message(user_id, "Розділ Воопоо поки в розробці.")

    elif text == t("pay_on_delivery_ru") or text == t("pay_on_delivery_ua"):
        bot.send_message(
            user_id,
            texts["pay_on_delivery_info_ru"] if lang == "ru" else texts["pay_on_delivery_info_ua"]
        )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(t("back_btn_ru") if lang == "ru" else t("back_btn_ua")))
        bot.send_message(
            user_id,
            t("back_btn_ru") if lang == "ru" else t("back_btn_ua"),
            reply_markup=markup
        )
        user_carts[user_id] = []

    elif text == t("pay_prepay_ru") or text == t("pay_prepay_ua"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(t("pay_done_ru") if lang == "ru" else t("pay_done_ua")))
        markup.add(types.KeyboardButton(t("back_btn_ru") if lang == "ru" else t("back_btn_ua")))
        bot.send_message(
            user_id,
            texts["prepay_info_ru"] if lang == "ru" else texts["prepay_info_ua"],
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif text == "Оплата криптовалютой" or text == "Оплата криптовалютою":
        crypto_wallet = "UQDjclQadIIq-DUoTNY53oHfcp9WVi5mRVnUVxVUnQ-vznEc (ton)"
        msg = (
            "💰 Оплата криптовалютой\n\n"
            f"Отправьте оплату на следующий адрес:\n`{crypto_wallet}`\n\n"
            "После оплаты нажмите кнопку ниже, чтобы подтвердить оплату."
            if lang == "ru"
            else
            "💰 Оплата криптовалютою\n\n"
            f"Відправте оплату на наступну адресу:\n`{crypto_wallet}`\n\n"
            "Після оплати натисніть кнопку нижче, щоб підтвердити оплату."
        )
        bot.send_message(user_id, msg, parse_mode="Markdown")

    elif text == t("pay_done_ru") or text == t("pay_done_ua"):
        try:
            user_mention = f"@{message.from_user.username or message.from_user.first_name}"
            bot.send_message(ADMIN_USERNAME, f"✅ Пользователь {user_mention} подтвердил оплату заказа.")
            bot.send_message(user_id, "Спасибо! Мы получили подтверждение оплаты. Ожидайте обработки заказа." if lang == "ru" else "Дякуємо! Ми отримали підтвердження оплати. Очікуйте обробки замовлення.")
        except Exception:
            pass

    elif text == t("clear_cart_ru") or text == t("clear_cart_ua"):
        user_carts[user_id] = []
        bot.send_message(user_id, "Корзина очищена." if lang == "ru" else "Кошик очищено.")

    elif text == t("menu_about", lang):
        bot.send_message(user_id, texts["about_ru"] if lang == "ru" else texts["about_ua"], parse_mode="Markdown")

    elif text == t("menu_partner", lang):
        count = len(referrals.get(user_id, []))
        spent = user_spending[user_id]
        ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        partner_text = (texts["partner_program_ru"] if lang == "ru" else texts["partner_program_ua"]).format(count=count, spent=spent, link=ref_link)
        bot.send_message(user_id, partner_text, parse_mode="Markdown")

    elif text == t("menu_orders", lang):
        bot.send_message(user_id, "История заказов пока недоступна." if lang == "ru" else "Історія замовлень поки недоступна.")

    elif text == t("menu_reviews", lang):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_view = types.KeyboardButton("📜 Посмотреть отзывы" if lang == "ru" else "📜 Переглянути відгуки")
        btn_write = types.KeyboardButton("🖊 Написать отзыв" if lang == "ru" else "🖊 Написати відгук")
        btn_back = types.KeyboardButton(t("back_btn_ru") if lang == "ru" else t("back_btn_ua"))
        markup.add(btn_view, btn_write)
        markup.add(btn_back)
        bot.send_message(user_id, "Выберите действие:" if lang == "ru" else "Оберіть дію:", reply_markup=markup)

    elif text == "📜 Посмотреть отзывы" or text == "📜 Переглянути відгуки":
        if reviews:
            all_reviews = "\n\n".join(reviews)
            bot.send_message(user_id, f"🗒 *Отзывы покупателей:*\n\n{all_reviews}" if lang == "ru" else f"🗒 *Відгуки покупців:*\n\n{all_reviews}", parse_mode="Markdown")
        else:
            bot.send_message(user_id, texts["reviews_list_empty_ru"] if lang == "ru" else texts["reviews_list_empty_ua"])

    elif text == "🖊 Написать отзыв" or text == "🖊 Написати відгук":
        bot.send_message(user_id, "✍ Напишите ваш отзыв здесь:" if lang == "ru" else "✍ Напишіть ваш відгук тут:")
        bot.register_next_step_handler(message, save_review)

    elif text == t("back_btn_ru") or text == t("back_btn_ua"):
        send_main_menu(message)

    else:
        bot.send_message(user_id, t("please_choose_ru") if lang == "ru" else t("please_choose_ua"))

def save_review(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    review_text = message.text.strip()
    if review_text:
        reviews.append(review_text)
        bot.send_message(user_id, texts["thank_review_ru"] if lang == "ru" else texts["thank_review_ua"])
    send_main_menu(message)
    
    # --- Каталог товаров ---

def show_catalog_menu(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == "ru":
        markup.add(
            types.KeyboardButton("💨 Под-системы"),
            types.KeyboardButton("🧃 Жидкости"),
            types.KeyboardButton("🔄 Картриджи"),
            types.KeyboardButton(t("back_btn_ru"))
        )
    else:
        markup.add(
            types.KeyboardButton("💨 Під-системи"),
            types.KeyboardButton("🧃 Рідини"),
            types.KeyboardButton("🔄 Картриджі"),
            types.KeyboardButton(t("back_btn_ua"))
        )
    bot.send_message(user_id, t("please_choose_ru") if lang == "ru" else t("please_choose_ua"), reply_markup=markup)

def show_cartridge_brands(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Vaporesso"),
        types.KeyboardButton("Voopoo"),
        types.KeyboardButton(t("back_btn_ru") if lang == "ru" else t("back_btn_ua"))
    )
    bot.send_message(user_id, "Выберите бренд картриджей:" if lang == "ru" else "Оберіть бренд картриджів:", reply_markup=markup)

def show_vaporesso_pods(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    markup = types.InlineKeyboardMarkup(row_width=1)

    pods = [
        ("Pod VAPORESSO Luxe 2", 450),
        ("Pod VAPORESSO Degree", 480),
        ("Pod VAPORESSO OSMALL", 350),
        ("Pod VAPORESSO XROS 3", 390),
    ]

    for name, price in pods:
        btn_text = f"{name} — {price} ₴"
        callback_data = f"add_to_cart|{name}|{price}"
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_data))

    markup.add(types.InlineKeyboardButton(t("back_btn_ru") if lang == "ru" else t("back_btn_ua"), callback_data="back_to_catalog"))
    bot.send_message(user_id, "Выберите товар для добавления в корзину:" if lang == "ru" else "Оберіть товар для додавання до кошика:", reply_markup=markup)

# --- Обработка inline кнопок ---

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")

    if call.data.startswith("add_to_cart"):
        _, product_name, price_str = call.data.split("|")
        price = int(price_str)
        user_carts[user_id].append((product_name, price))
        bot.answer_callback_query(call.id, text="Добавлено в корзину!" if lang == "ru" else "Додано до кошика!")

    elif call.data == "back_to_catalog":
        show_catalog_menu(call.message)

# --- Корзина ---

def show_cart(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    cart = user_carts[user_id]

    if not cart:
        bot.send_message(user_id, texts["cart_empty_ru"] if lang == "ru" else texts["cart_empty_ua"])
        return

    lines = []
    total = 0
    for i, (name, price) in enumerate(cart, 1):
        lines.append(f"{i}. {name} — {price} ₴")
        total += price
    text = (texts["cart_title_ru"] if lang == "ru" else texts["cart_title_ua"]) + "\n".join(lines) + (texts["cart_total_ru"] if lang == "ru" else texts["cart_total_ua"]).format(total=total)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(t("order_button_ru") if lang == "ru" else t("order_button_ua")))
    markup.add(types.KeyboardButton(t("clear_cart_ru") if lang == "ru" else t("clear_cart_ua")))
    markup.add(types.KeyboardButton(t("back_btn_ru") if lang == "ru" else t("back_btn_ua")))
    bot.send_message(user_id, text, reply_markup=markup)

# --- Оформление заказа ---

@bot.message_handler(func=lambda m: m.text in [texts["order_button_ru"], texts["order_button_ua"]])
def order_handler(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    cart = user_carts[user_id]
    if not cart:
        bot.send_message(user_id, texts["cart_empty_ru"] if lang == "ru" else texts["cart_empty_ua"])
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(t("pay_on_delivery_ru") if lang == "ru" else t("pay_on_delivery_ua")),
        types.KeyboardButton(t("pay_prepay_ru") if lang == "ru" else t("pay_prepay_ua")),
    )
    bot.send_message(user_id, t("pay_method_ru") if lang == "ru" else t("pay_method_ua"), reply_markup=markup)

    # Добавим сумму к покупкам реферера
    amount = sum(price for _, price in cart)
    user_spending[user_id] += amount
    if user_id in user_referrer:
        referrer_id = user_referrer[user_id]
        user_spending[referrer_id] += amount
        try:
            bot.send_message(referrer_id,
                             (texts["referral_purchase_ru"] if lang == "ru" else texts["referral_purchase_ua"]).format(
                                 user=f"@{message.from_user.username or message.from_user.first_name}",
                                 amount=amount,
                                 total=user_spending[referrer_id]))
        except Exception:
            pass

bot.infinity_polling()
