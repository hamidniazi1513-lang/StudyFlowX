import os
import pytesseract

from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


last_image_text = {}


def register_image_handlers(bot):

    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):

        try:

            file_info = bot.get_file(message.photo[-1].file_id)

            downloaded_file = bot.download_file(file_info.file_path)

            image_path = f"temp_{message.chat.id}.jpg"

            with open(image_path, "wb") as new_file:

                new_file.write(downloaded_file)

            extracted_text = pytesseract.image_to_string(
                Image.open(image_path)
            )

            last_image_text[str(message.chat.id)] = extracted_text

            os.remove(image_path)

            if not extracted_text.strip():

                bot.send_message(
                    message.chat.id,
                    "⚠ No readable text found in image."
                )

        except Exception as e:

            bot.send_message(
                message.chat.id,
                f"❌ OCR Error:\n{e}"
            )