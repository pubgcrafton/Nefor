# █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
# █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█
#
#              © Copyright 2022
#
#          https://t.me/hikariatama
#
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

import logging
import os
from random import choice

from .. import loader, translations
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)
imgs = [
    "https://siasky.net/_AydMH2r41XBCQBMlZsIK3-cBf2EBwAM4Ue7vbkG0XnzoA",
    "https://siasky.net/_AydMH2r41XBCQBMlZsIK3-cBf2EBwAM4Ue7vbkG0XnzoA",
    "https://siasky.net/_AydMH2r41XBCQBMlZsIK3-cBf2EBwAM4Ue7vbkG0XnzoA",
    "https://siasky.net/_AydMH2r41XBCQBMlZsIK3-cBf2EBwAM4Ue7vbkG0XnzoA",
    "https://siasky.net/_AydMH2r41XBCQBMlZsIK3-cBf2EBwAM4Ue7vbkG0XnzoA",
    "https://siasky.net/_AydMH2r41XBCQBMlZsIK3-cBf2EBwAM4Ue7vbkG0XnzoA",
    "https://siasky.net/_AydMH2r41XBCQBMlZsIK3-cBf2EBwAM4Ue7vbkG0XnzoA",
]

TEXT = """😺🇬🇧 <b>Hello.</b> You've just installed <b>Nino</b> userbot.

❓ <b>Need help?</b> Feel free to join our support chat. We help <b>everyone</b>.

📼 <b>Official modules sources:</b>
▫️ @nino_mods
▫️ @umodules
▫️ <code>.dlmod</code>

✅ <b>Trusted modules' developers:</b>
▫️ @morisummermods
▫️ @cakestwix_mods

🌐 Поменяй язык на русский <code>.setlang ru</code>
"""


TEXT_RU = """😊 <b>Мы рады</b> что вы установили нашего бота <b>Nino</b>.

❓ <b>Нужна помощь?</b> Вступай в наш чат поддержки. Мы помогаем <b>всем</b>.

▪️ <b>Официальные источники модулей:</b>
▫️ @nino_mods
▫️ @umodules
▫️ <code>.dlmod</code>

🧑‍🎤 Модератор: @the_farkhodov
🧑‍🎤 Канал: @ninoall
🧑‍🎤 Чат помощи: @nino_talks

▪️ <b>Также ты можешь найти модули тут:</b>
▫️ @morisummermods
▫️ @cakestwix_mods
"""

if "OKTETO" in os.environ:
    TEXT += "☁️ <b>Your userbot is installed on Okteto</b>. You will get notifications from @WebpageBot. Do not block him."
    TEXT_RU += "☁️ <b>Твой юзербот установлен на Okteto</b>. Ты будешь получать уведомления от @WebpageBot. Не блокируй его."

if "DYNO" in os.environ:
    TEXT += "♓️ <b>Your userbot is installed on Heroku</b>. You will get notifications from @WebpageBot. Do not block him."
    TEXT_RU += "♓️ <b>Твой юзербот установлен на Heroku</b>. Ты будешь получать уведомления от @WebpageBot. Не блокируй его."


@loader.tds
class QuickstartMod(loader.Module):
    """Notifies user about userbot installation"""

    strings = {"name": "Quickstart"}

    async def client_ready(self, client, db):
        self._db = db

        if db.get("hikka", "disable_quickstart", False):
            raise loader.SelfUnload

        mark = self.inline.generate_markup(
            [
                [{"text": "🥷 Support chat", "url": "https://t.me/nino_talks"}],
                [{"text": "🇷🇺 Русский", "data": "hikka_qs_sw_lng_ru"}],
            ]
        )

        await self.inline.bot.send_animation(
            self._tg_id,
            animation=choice(imgs),
            caption=TEXT,
            reply_markup=mark,
        )

        db.set("hikka", "disable_quickstart", True)

    async def quickstart_callback_handler(self, call: InlineCall):
        if not call.data.startswith("hikka_qs_sw_lng_"):
            return

        lang = call.data.split("_")[-1]
        if lang == "ru":
            mark = self.inline.generate_markup(
                [
                    [{"text": "🥷 Чат помощи", "url": "https://t.me/nino_talks"}],
                    [{"text": "🇬🇧 English", "data": "hikka_qs_sw_lng_en"}],
                ]
            )

            self._db.set(translations.__name__, "lang", "ru")
            self._db.set(translations.__name__, "pack", "ru")
            await self.translator.init()
            await call.answer("🇷🇺 Язык сохранен!")

            await self.inline.bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=TEXT_RU,
                reply_markup=mark,
            )
        elif lang == "en":
            mark = self.inline.generate_markup(
                [
                    [{"text": "🥷 Support chat", "url": "https://t.me/nino_talks"}],
                    [{"text": "🇷🇺 Русский", "data": "hikka_qs_sw_lng_ru"}],
                ]
            )

            self._db.set(translations.__name__, "lang", "en")
            self._db.set(translations.__name__, "pack", None)
            await self.translator.init()
            await call.answer("🇬🇧 Language saved!")

            await self.inline.bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                caption=TEXT,
                reply_markup=mark,
            )
