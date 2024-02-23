from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler

TOKEN = '6774933123:AAE4fbID1LhzJY4vJiTGoaHG17mM7tGXHwc'

# Mock database of stock names (replace with your actual database)
mock_stock_database = ["Stock1", "Stock2", "Stock3"]

# Dictionary to store user subscriptions
user_subscriptions = {}

def start(update: Update, context: CallbackContext) -> None:
    # Create a custom keyboard with "Мои подписки" and "Подписаться" buttons
    keyboard = [
        [KeyboardButton("Мои подписки"), KeyboardButton("Подписаться")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Send the message with the custom keyboard
    update.message.reply_text("Привет! Чтобы подписаться на акцию, нажмите кнопку 'Подписаться'.", reply_markup=reply_markup)

def subscribe(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Напишите название акции, на которую хотите подписаться:")

def check_stock(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    chat_id = update.message.chat_id

    if user_input == "Мои подписки":
        show_subscriptions(update, context)
    elif user_input == "Подписаться":
        subscribe(update, context)
    else:
        # Check if the user input is in the stock database
        if user_input in mock_stock_database:
            subscriptions = user_subscriptions.get(chat_id, [])
            if user_input in subscriptions:
                update.message.reply_text(f"Вы уже подписаны на акцию {user_input}")
            else:
                # Subscribe the user to the stock
                user_subscriptions[chat_id] = user_subscriptions.get(chat_id, []) + [user_input]
                update.message.reply_text(f"Вы успешно подписаны на акцию {user_input}")
        else:
            update.message.reply_text("Извините, не можем подписать вас на эту акцию. "
                                    "Проверьте правильность написания названия акции.")

def show_subscriptions(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    subscriptions = user_subscriptions.get(chat_id, [])

    if subscriptions:
        update.message.reply_text(f"Вы подписаны на следующие акции: {', '.join(subscriptions)}")
    else:
        update.message.reply_text("Вы пока не подписаны ни на одну акцию.")

def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("subscriptions", show_subscriptions))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.reply, check_stock))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
