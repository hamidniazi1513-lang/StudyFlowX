def register_translation_handlers(bot, client):

    @bot.message_handler(func=lambda message: message.text == "🌐 Translate")
    def translate_menu(message):

        bot.send_message(
            message.chat.id,
            "🌐 Send text like:\n\ntranslate hello to pashto"
        )

    @bot.message_handler(func=lambda message: message.text.lower().startswith("translate"))
    def translate_text(message):

        user_text = message.text

        bot.send_message(
            message.chat.id,
            "🌐 Translating..."
        )

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a translator. Translate accurately and only give translated text."
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            )

            translated = response.choices[0].message.content

            bot.send_message(
                message.chat.id,
                f"🌐 Translation:\n\n{translated}"
            )

        except Exception as e:

            bot.send_message(
                message.chat.id,
                f"❌ Error:\n{e}"
            )