import os
import re
import pytesseract

from telebot import types
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


waiting_for_quiz_image = {}

quiz_question_count = {}

quiz_data = {}
quiz_scores = {}
quiz_answers = {}
user_answers = {}


def register_quiz_handlers(bot, client):

    @bot.message_handler(func=lambda message: message.text == "❓ Quiz")
    def start_quiz(message):

        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True
        )

        btn_5 = types.KeyboardButton("5")
        btn_10 = types.KeyboardButton("10")
        btn_20 = types.KeyboardButton("20")
        btn_30 = types.KeyboardButton("30")

        markup.add(btn_5, btn_10)
        markup.add(btn_20, btn_30)

        waiting_for_quiz_image[message.chat.id] = "count"

        bot.send_message(
            message.chat.id,
            "🧠 How many quiz questions do you want?",
            reply_markup=markup
        )

    @bot.message_handler(
        func=lambda message:
        waiting_for_quiz_image.get(message.chat.id) == "count"
    )
    def save_question_count(message):

        if message.text not in ["5", "10", "20", "30"]:

            bot.send_message(
                message.chat.id,
                "❌ Please choose: 5, 10, 20, or 30"
            )

            return

        quiz_question_count[message.chat.id] = int(message.text)

        waiting_for_quiz_image[message.chat.id] = True

        bot.send_message(
            message.chat.id,
            "📚 Send your study material.\n\n"
            "You can send:\n"
            "• Text messages\n"
            "• Lecture screenshots\n"
            "• Notes images\n"
            "• Textbook photos\n\n"
            "🧠 AI will automatically create a quiz for you."
        )

    @bot.message_handler(content_types=['photo'])
    def process_quiz_image(message):

        if not waiting_for_quiz_image.get(message.chat.id):

            return

        waiting_for_quiz_image.pop(message.chat.id, None)

        user_id = str(message.chat.id)

        question_count = quiz_question_count.get(
            message.chat.id,
            5
        )

        bot.send_message(
            message.chat.id,
            f"🧠 Creating {question_count}-question AI quiz from image...\n"
            "Please wait a moment."
        )

        file_info = bot.get_file(message.photo[-1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        image_path = f"quiz_{message.chat.id}.jpg"

        with open(image_path, "wb") as new_file:

            new_file.write(downloaded_file)

        notes_text = pytesseract.image_to_string(
            Image.open(image_path)
        )

        os.remove(image_path)

        if not notes_text.strip():

            bot.send_message(
                message.chat.id,
                "❌ Could not extract readable text from image."
            )

            return

        generate_quiz(
            bot,
            client,
            message.chat.id,
            notes_text,
            question_count
        )

    @bot.message_handler(
        func=lambda message:
        waiting_for_quiz_image.get(message.chat.id) == True
        and message.content_type == "text"
    )
    def process_quiz_text(message):

        waiting_for_quiz_image.pop(message.chat.id, None)

        user_id = str(message.chat.id)

        question_count = quiz_question_count.get(
            message.chat.id,
            5
        )

        notes_text = message.text

        bot.send_message(
            message.chat.id,
            f"🧠 Creating {question_count}-question AI quiz from text...\n"
            "Please wait a moment."
        )

        generate_quiz(
            bot,
            client,
            message.chat.id,
            notes_text,
            question_count
        )

    @bot.message_handler(
        func=lambda message:
        message.text.upper() in ["A", "B", "C", "D"]
    )
    def handle_answer(message):

        user_id = str(message.chat.id)

        if user_id not in quiz_data:

            return

        current_index = quiz_answers[user_id]

        current_question = quiz_data[user_id][current_index]

        user_answer = message.text.upper()

        user_answers[user_id].append(
            {
                "question_number": current_index + 1,
                "user_answer": user_answer,
                "correct_answer": current_question["answer"]
            }
        )

        if user_answer == current_question["answer"]:

            quiz_scores[user_id] += 1

        quiz_answers[user_id] += 1

        if quiz_answers[user_id] < len(quiz_data[user_id]):

            send_question(bot, message.chat.id)

        else:

            score = quiz_scores[user_id]

            total_questions = len(quiz_data[user_id])

            percentage = (
                score / total_questions
            ) * 100

            if percentage >= 80:

                performance = "Excellent 🔥"

            elif percentage >= 60:

                performance = "Good 👍"

            else:

                performance = "Needs Improvement 📚"

            review_text = ""

            for item in user_answers[user_id]:

                if item["user_answer"] == item["correct_answer"]:

                    review_text += (
                        f"Q{item['question_number']} → "
                        f"✅ Correct\n"
                    )

                else:

                    review_text += (
                        f"Q{item['question_number']} → "
                        f"❌ Wrong "
                        f"(Correct: {item['correct_answer']})\n"
                    )

            bot.send_message(
                message.chat.id,
                f"🎯 Quiz Finished!\n\n"
                f"✅ Correct Answers: {score}\n"
                f"❌ Wrong Answers: {total_questions - score}\n"
                f"📊 Score: {percentage:.0f}%\n"
                f"🏆 Performance: {performance}\n\n"
                f"📝 Answer Review\n\n"
                f"{review_text}"
            )

            del quiz_data[user_id]
            del quiz_scores[user_id]
            del quiz_answers[user_id]
            del user_answers[user_id]


def generate_quiz(bot, client, chat_id, notes_text, question_count):

    user_id = str(chat_id)

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Create exactly {question_count} "
                        "university-level multiple choice quiz questions "
                        "from the study material.\n\n"

                        "STRICT RULES:\n"
                        "- Each question must have 4 options.\n"
                        "- Use different correct answers.\n"
                        "- Correct answers must NOT all be B.\n"
                        "- Mix answers between A, B, C, and D.\n"
                        "- Output ONLY in this exact format.\n\n"

                        "Q1: question\n"
                        "A) option\n"
                        "B) option\n"
                        "C) option\n"
                        "D) option\n"
                        "ANSWER: A\n\n"

                        "Repeat the same structure for all questions."
                    )
                },
                {
                    "role": "user",
                    "content": notes_text
                }
            ]
        )

        quiz_text = response.choices[0].message.content

        questions = re.split(r"Q\d+:", quiz_text)[1:]

        parsed_questions = []

        for q in questions:

            lines = q.strip().split("\n")

            question = lines[0]

            options = lines[1:5]

            answer_line = lines[-1]

            correct_answer = (
                answer_line.replace("ANSWER:", "")
                .replace(".", "")
                .replace(")", "")
                .strip()
                .upper()[0]
            )

            parsed_questions.append(
                {
                    "question": question,
                    "options": options,
                    "answer": correct_answer
                }
            )

        quiz_data[user_id] = parsed_questions
        quiz_scores[user_id] = 0
        quiz_answers[user_id] = 0
        user_answers[user_id] = []

        send_question(bot, chat_id)

    except Exception as e:

        bot.send_message(
            chat_id,
            f"❌ Quiz generation error:\n{e}"
        )


def send_question(bot, chat_id):

    user_id = str(chat_id)

    current_index = quiz_answers[user_id]

    question_data = quiz_data[user_id][current_index]

    question_text = (
        f"❓ Question {current_index + 1}/{len(quiz_data[user_id])}\n\n"
        f"{question_data['question']}\n\n"
        f"{question_data['options'][0]}\n"
        f"{question_data['options'][1]}\n"
        f"{question_data['options'][2]}\n"
        f"{question_data['options'][3]}"
    )

    bot.send_message(
        chat_id,
        question_text
    )