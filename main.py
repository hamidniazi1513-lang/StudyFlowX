import telebot
from telebot import types
import time
import threading
from groq import Groq

from gpa_system import register_gpa_handlers
from admin_system import register_admin_handlers
from translation_system import register_translation_handlers
from ai_system import register_ai_handlers
from image_system import register_image_handlers
from database import conn, cursor
from quiz_system import register_quiz_handlers


BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

client = Groq(
    api_key="YOUR_GROQ_API_KEY"
)
class Assistant:

    def __init__(self, name):

        self.name = name

    def welcome_message(self):

        return f"🤖 Welcome to {self.name}!"


class StudentAssistant(Assistant):

    def __init__(self, name):

        super().__init__(name)

    def format_note(self, note):

        return f"📝 {note}"

    def welcome_message(self):

        return f"🤖 Welcome to {self.name}!"

assistant = StudentAssistant("StudyFlowX")


waiting_for_note = {}
waiting_for_reminder = {}
waiting_for_reminder_time = {}
reminder_texts = {}

ADMIN_ID = 7729584564
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cursor.execute(
        "INSERT OR IGNORE INTO users (chat_id) VALUES (?)",
        (message.chat.id,)
    )

    conn.commit()
    schedule_btn = types.KeyboardButton("📚 Schedule")
    quiz_btn = types.KeyboardButton("❓ Quiz")
    notes_btn = types.KeyboardButton("📝 Notes")
    view_notes_btn = types.KeyboardButton("📚 View Notes")
    delete_notes_btn = types.KeyboardButton("🗑 Delete Notes")
    reminder_btn = types.KeyboardButton("⏰ Reminder")
    gpa_btn = types.KeyboardButton("📊 GPA")
    translate_btn = types.KeyboardButton("🌐 Translate")

    markup.add(schedule_btn, quiz_btn)
    markup.add(notes_btn, view_notes_btn)
    markup.add(delete_notes_btn, reminder_btn)
    markup.add(gpa_btn)
    markup.add(translate_btn)

    bot.send_message(
        message.chat.id,
        f"{assistant.welcome_message()}\n\nChoose an option below:",
        reply_markup=markup
    )
waiting_for_schedule = {}


@bot.message_handler(func=lambda message: message.text == "📚 Schedule")
def schedule_menu(message):

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    add_btn = types.KeyboardButton("➕ Add Schedule")
    view_btn = types.KeyboardButton("📖 View Schedule")
    delete_btn = types.KeyboardButton("🗑 Delete Schedule")
    back_btn = types.KeyboardButton("⬅ Back")

    markup.add(add_btn, view_btn)
    markup.add(delete_btn)
    markup.add(back_btn)

    bot.send_message(
        message.chat.id,
        "📅 Schedule Manager",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "➕ Add Schedule")
def add_schedule(message):

    waiting_for_schedule[message.chat.id] = True

    bot.send_message(
        message.chat.id,
        "📚 Send your class in this format:\n\n"
        "Monday | Programming | 09:00 AM"
    )


@bot.message_handler(func=lambda message: waiting_for_schedule.get(message.chat.id) == True)
def save_schedule(message):

    try:

        data = message.text.split("|")

        day = data[0].strip()
        subject = data[1].strip()
        class_time = data[2].strip()

        cursor.execute(
            """
            INSERT INTO schedules
            (chat_id, day, subject, time)
            VALUES (?, ?, ?, ?)
            """,
            (
                message.chat.id,
                day,
                subject,
                class_time
            )
        )

        conn.commit()

        waiting_for_schedule.pop(
            message.chat.id,
            None
        )

        bot.send_message(
            message.chat.id,
            "✅ Schedule added successfully."
        )

    except:

        bot.send_message(
            message.chat.id,
            "❌ Invalid format.\n\n"
            "Example:\n"
            "Monday | Programming | 09:00 AM"
        )


@bot.message_handler(func=lambda message: message.text == "📖 View Schedule")
def view_schedule(message):

    cursor.execute(
        """
        SELECT day, subject, time
        FROM schedules
        WHERE chat_id = ?
        ORDER BY day
        """,
        (message.chat.id,)
    )

    schedules = cursor.fetchall()

    if not schedules:

        bot.send_message(
            message.chat.id,
            "❌ No schedules found."
        )

        return

    text = "📅 Your Schedule\n\n"

    for schedule in schedules:

        text += (
            f"📚 {schedule[0]}\n"
            f"• {schedule[1]}\n"
            f"⏰ {schedule[2]}\n\n"
        )

    bot.send_message(
        message.chat.id,
        text
    )


@bot.message_handler(func=lambda message: message.text == "🗑 Delete Schedule")
def delete_schedule(message):

    cursor.execute(
        """
        DELETE FROM schedules
        WHERE chat_id = ?
        """,
        (message.chat.id,)
    )

    conn.commit()

    bot.send_message(
        message.chat.id,
        "🗑 All schedules deleted."
    )
@bot.message_handler(func=lambda message: message.text == "📝 Notes")
def notes(message):

    waiting_for_note[message.chat.id] = True

    bot.send_message(
        message.chat.id,
        "📝 Send your note now."
    )

@bot.message_handler(func=lambda message: waiting_for_note.get(message.chat.id) == True)
def save_note(message):

    note_text = message.text

    cursor.execute(
        "INSERT INTO notes (chat_id, note) VALUES (?, ?)",
        (message.chat.id, note_text)
    )

    conn.commit()

    waiting_for_note.pop(message.chat.id, None)

    bot.send_message(
        message.chat.id,
        f"✅ Note saved:\n\n{note_text}"
    )
@bot.message_handler(func=lambda message: message.text == "⏰ Reminder")
def reminder(message):

    waiting_for_reminder[message.chat.id] = True

    bot.send_message(
        message.chat.id,
        "⏰ Send your reminder text."
    )


@bot.message_handler(func=lambda message: waiting_for_reminder.get(message.chat.id) == True)
def save_reminder_text(message):

    reminder_texts[message.chat.id] = message.text

    waiting_for_reminder.pop(message.chat.id, None)

    waiting_for_reminder_time[message.chat.id] = True

    bot.send_message(
        message.chat.id,
        "⏰ Send reminder time in seconds.\n\nExample:\n60"
    )


def send_reminder(chat_id, text, seconds):

    time.sleep(seconds)

    bot.send_message(
        chat_id,
        f"⏰ Reminder:\n\n{text}"
    )


@bot.message_handler(func=lambda message: waiting_for_reminder_time.get(message.chat.id) == True)
def save_reminder_time(message):

    try:

        seconds = int(message.text)

        waiting_for_reminder_time.pop(message.chat.id, None)

        reminder_text = reminder_texts.get(message.chat.id)

        threading.Thread(
            target=send_reminder,
            args=(message.chat.id, reminder_text, seconds)
        ).start()

        bot.send_message(
            message.chat.id,
            f"✅ Reminder set for {seconds} seconds."
        )

    except:

        bot.send_message(
            message.chat.id,
            "❌ Please enter a valid number.\n\nExample:\n60"
        )
@bot.message_handler(func=lambda message: message.text == "📚 View Notes")
def view_notes(message):

    cursor.execute(
        "SELECT note FROM notes WHERE chat_id = ?",
        (message.chat.id,)
    )

    notes = cursor.fetchall()

    if notes:

        all_notes = ""

        for note in notes:
            all_notes += f"• {note[0]}\n\n"

        bot.send_message(
            message.chat.id,
            f"📚 Your Notes:\n\n{all_notes}"
        )

    else:

        bot.send_message(
            message.chat.id,
            "❌ No notes saved yet."
        )
@bot.message_handler(func=lambda message: message.text == "🗑 Delete Notes")
def delete_notes(message):

    cursor.execute(
        "DELETE FROM notes WHERE chat_id = ?",
        (message.chat.id,)
    )

    conn.commit()

    bot.send_message(
        message.chat.id,
        "🗑 All notes deleted from database."
    )
@bot.message_handler(func=lambda message: message.text == "⬅ Back")
def back_to_main(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    schedule_btn = types.KeyboardButton("📚 Schedule")
    quiz_btn = types.KeyboardButton("❓ Quiz")
    notes_btn = types.KeyboardButton("📝 Notes")
    view_notes_btn = types.KeyboardButton("📚 View Notes")
    delete_notes_btn = types.KeyboardButton("🗑 Delete Notes")
    reminder_btn = types.KeyboardButton("⏰ Reminder")
    gpa_btn = types.KeyboardButton("📊 GPA")
    translate_btn = types.KeyboardButton("🌐 Translate")

    markup.add(schedule_btn, quiz_btn)
    markup.add(notes_btn, view_notes_btn)
    markup.add(delete_notes_btn, reminder_btn)
    markup.add(gpa_btn)
    markup.add(translate_btn)
    bot.send_message(
        message.chat.id,
        "Main menu:",
        reply_markup=markup
    )

register_gpa_handlers(bot)
register_admin_handlers(bot, cursor, conn, ADMIN_ID)
register_translation_handlers(bot, client)
register_ai_handlers(bot, client)
register_quiz_handlers(bot, client)


print("Bot is running...")

bot.polling()