import telebot
from telebot import types

TOKEN = "6639711517:AAGLNJnu0R9KNAlcvDxhrX2wfJWCgfLSaiI"
bot = telebot.TeleBot(TOKEN)

tasks = []


def generate_inline_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Add", callback_data="add"),
               types.InlineKeyboardButton("List", callback_data="list"),
               types.InlineKeyboardButton("Delete", callback_data="delete"))
    return markup


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to the to-do list Telegram bot :)\n"
                                      "Use the buttons below to manage your tasks.",
                     reply_markup=generate_inline_keyboard())


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "This is a to-do list Telegram bot.\n"
                                      "Use the following commands:\n"
                                      "/add - Add a new task\n"
                                      "/list - List tasks\n"
                                      "/delete - Delete a task\n"
                                      "/start - Show main menu\n"
                                      "/help - Show help menu")


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "/add":
        bot.send_message(message.chat.id, "Enter a task to add:")
        bot.register_next_step_handler(message, add_task)
    elif message.text == "/list":
        list_tasks(message)
    elif message.text == "/delete":
        delete_task(message)
    else:
        bot.send_message(message.chat.id, "Invalid input. Please use the buttons or commands.",
                         reply_markup=generate_inline_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "add":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Enter a task to add:", reply_markup=None)
        bot.register_next_step_handler(call.message, add_task)
    elif call.data == "list":
        list_tasks(call.message)
    elif call.data == "delete":
        delete_task(call.message)


def add_task(message):
    task = message.text
    tasks.append(task)
    bot.send_message(message.chat.id, f"Task '{task}' added to the list.",
                     reply_markup=generate_inline_keyboard())


def list_tasks(message):
    if not tasks:
        bot.send_message(message.chat.id, "There are no tasks currently.",
                         reply_markup=generate_inline_keyboard())
    else:
        response = "Current Tasks:\n"
        for index, task in enumerate(tasks):
            response += f"Task #{index}. {task}\n"
        bot.send_message(message.chat.id, response, reply_markup=generate_inline_keyboard())


def delete_task(message):
    if not tasks:
        bot.send_message(message.chat.id, "There are no tasks to delete.",
                         reply_markup=generate_inline_keyboard())
        return

    response = "Current Tasks:\n"
    for index, task in enumerate(tasks):
        response += f"Task #{index}. {task}\n"
    bot.send_message(message.chat.id, response, reply_markup=generate_inline_keyboard())

    msg = bot.send_message(message.chat.id, "Enter the # to delete:")
    bot.register_next_step_handler(msg, process_delete_task)


def process_delete_task(message):
    try:
        task_to_delete = int(message.text)
        if 0 <= task_to_delete < len(tasks):
            deleted_task = tasks.pop(task_to_delete)
            bot.send_message(message.chat.id, f"Task '{deleted_task}' has been removed.",
                             reply_markup=generate_inline_keyboard())
        else:
            bot.send_message(message.chat.id, f"Task #{task_to_delete} was not found.",
                             reply_markup=generate_inline_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "Invalid input. Please enter a valid task number to delete.",
                         reply_markup=generate_inline_keyboard())


if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
