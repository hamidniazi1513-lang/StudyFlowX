def register_admin_handlers(bot, cursor, conn, ADMIN_ID):

    @bot.message_handler(commands=['admin'])
    def admin_panel(message):

        if message.chat.id != ADMIN_ID:

            bot.send_message(
                message.chat.id,
                "⛔ Access denied.\nYou are not the admin."
            )

            return

        admin_text = (
            "👨‍💻 ADMIN PANEL\n\n"
            "🔹 /users → View total users\n"
            "🔹 /broadcast → Send message to all users\n"
            "🔹 /admin → Open admin panel\n\n"
            "✅ System Status: Online\n"
            "🤖 StudyFlowX Management System"
        )

        bot.send_message(
            message.chat.id,
            admin_text
        )

    @bot.message_handler(commands=['users'])
    def total_users(message):

        if message.chat.id != ADMIN_ID:

            bot.send_message(
                message.chat.id,
                "⛔ Access denied."
            )

            return

        cursor.execute("SELECT COUNT(*) FROM users")

        total = cursor.fetchone()[0]

        bot.send_message(
            message.chat.id,
            f"👥 Total Bot Users: {total}"
        )

    @bot.message_handler(commands=['broadcast'])
    def broadcast_message(message):

        if message.chat.id != ADMIN_ID:

            bot.send_message(
                message.chat.id,
                "⛔ Access denied."
            )

            return

        text = message.text.replace("/broadcast", "").strip()

        if not text:

            bot.send_message(
                message.chat.id,
                "❌ Usage:\n/broadcast Your message"
            )

            return

        cursor.execute("SELECT chat_id FROM users")

        users = cursor.fetchall()

        sent_count = 0

        for user in users:

            try:

                bot.send_message(
                    user[0],
                    f"📢 ADMIN MESSAGE\n\n{text}"
                )

                sent_count += 1

            except:
                pass

        bot.send_message(
            message.chat.id,
            f"✅ Broadcast sent to {sent_count} users."
        )