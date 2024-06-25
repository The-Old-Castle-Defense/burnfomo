import traceback

import telegram
from telegram import Bot


class TGBot:
    bot = None
    log_channel = None

    def init(self, token, log_channel):
        self.bot = Bot(token)
        self.log_channel = log_channel


    def send_to_logs(self, text, parse_mode=None):
        try:
            self.bot.send_message(
                self.log_channel,
                text=text,
                disable_web_page_preview=True,
                parse_mode=parse_mode
            )
        except Exception as exc:
            print(exc)



    def send_message(self, user_id, text, parse_mode=None, disable_web_page_preview=None, reply_markup=None, timeout=5):
        try:
            response = self.bot.send_message(
                user_id,
                text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
                timeout=timeout
            )
            print(response)
            return response
        except telegram.error.Unauthorized as exc:
            print(exc)
        except Exception as exc:
            print(exc)

    def delete_message(self, user_id, msg_id):
        try:
            self.bot.delete_message(
                user_id,
                msg_id,
            )
        except Exception as exc:
            print(exc)



    def send_photo(self, user_id, photo, parse_mode=None, caption=None, reply_markup=None, timeout=200):
        try:
            response = self.bot.send_photo(
                user_id,
                photo,
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                timeout=timeout
            )
            return response
        except telegram.error.Unauthorized as exc:
            pass
        except Exception as exc:
            print(exc)
            self.send_to_logs(traceback.format_exc() + f"{str(photo)}")
