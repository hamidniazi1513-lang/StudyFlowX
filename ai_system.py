import json
from image_system import last_image_text

MEMORY_FILE = "memory.json"


try:

    with open(MEMORY_FILE, "r") as file:

        chat_memory = json.load(file)

except:

    chat_memory = {}


def save_memory():

    with open(MEMORY_FILE, "w") as file:

        json.dump(chat_memory, file, indent=4)


def register_ai_handlers(bot, client):

    @bot.message_handler(func=lambda message: message.text.startswith("/ai"))
    def ai_chat(message):

        user_text = message.text.replace("/ai", "").strip()

        user_id = str(message.chat.id)

        if user_id not in chat_memory:

            chat_memory[user_id] = []

        if not user_text:

            bot.send_message(
                message.chat.id,
                "🤖 Please write something after /ai"
            )

            return

        if "image" in user_text.lower():

            image_text = last_image_text.get(user_id, "")

            combined_text = (
                f"{user_text}\n\n"
                f"Image Text:\n{image_text}"
            )

        else:

            combined_text = user_text

        chat_memory[user_id].append(
            {
                "role": "user",
                "content": combined_text
            }
        )
        save_memory()

        bot.send_message(
            message.chat.id,
            "🤖 Thinking..."
        )

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a smart student assistant with memory. "
                            "Remember previous conversation context. "
                            "Give short, accurate, and direct answers. "
                            "If uncertain, say you are not sure."
                        )
                    }
                ] + chat_memory[user_id]
            )

            ai_reply = response.choices[0].message.content

            chat_memory[user_id].append(
                {
                    "role": "assistant",
                    "content": ai_reply
                }
            )

            save_memory()

            bot.send_message(
                message.chat.id,
                f"🤖 AI:\n\n{ai_reply}"
            )

        except Exception as e:

            bot.send_message(
                message.chat.id,
                f"❌ Error:\n{e}"
            )