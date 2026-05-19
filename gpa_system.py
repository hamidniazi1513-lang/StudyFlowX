from telebot import types


waiting_for_gpa = {}


def register_gpa_handlers(bot):

    @bot.message_handler(func=lambda message: message.text == "📊 GPA")
    def gpa(message):

        waiting_for_gpa[message.chat.id] = True

        bot.send_message(
            message.chat.id,
            "📊 Enter your subject scores separated by spaces\n\nExample:\n90 85 78 95"
        )

    @bot.message_handler(func=lambda message: waiting_for_gpa.get(message.chat.id) == True)
    def save_gpa(message):

        try:

            scores = list(map(float, message.text.split()))

            average = sum(scores) / len(scores)

            if average >= 95:
                gpa = 4.0
                letter = "A"
                performance = "Excellent 🔥"

            elif average >= 90:
                gpa = 3.67
                letter = "A-"
                performance = "Excellent 🔥"

            elif average >= 85:
                gpa = 3.33
                letter = "B+"
                performance = "Good 👍"

            elif average >= 80:
                gpa = 3.0
                letter = "B"
                performance = "Good 👍"

            elif average >= 75:
                gpa = 2.67
                letter = "B-"
                performance = "Good 👍"

            elif average >= 70:
                gpa = 2.33
                letter = "C+"
                performance = "Satisfactory 🙂"

            elif average >= 65:
                gpa = 2.0
                letter = "C"
                performance = "Satisfactory 🙂"

            elif average >= 60:
                gpa = 1.67
                letter = "C-"
                performance = "Satisfactory 🙂"

            elif average >= 55:
                gpa = 1.33
                letter = "D+"
                performance = "Pass 🙂"

            elif average >= 50:
                gpa = 1.0
                letter = "D"
                performance = "Pass 🙂"

            elif average >= 25:
                gpa = 0
                letter = "FX"
                performance = "Fail ❌"

            else:
                gpa = 0
                letter = "F"
                performance = "Fail ❌"

            waiting_for_gpa.pop(message.chat.id, None)

            bot.send_message(
                message.chat.id,
                f"📚 Subjects: {len(scores)}\n"
                f"📊 Average Score: {average:.2f}\n"
                f"🎓 GPA: {gpa}\n"
                f"📄 Letter Grade: {letter}\n"
                f"🏅 Performance: {performance}"
            )

        except:

            bot.send_message(
                message.chat.id,
                "❌ Invalid format.\n\nExample:\n90 85 78 95"
            )