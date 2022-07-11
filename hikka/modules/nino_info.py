#    ░█████╗░███╗░░░███╗░█████╗░██████╗░███████╗
#    ██╔══██╗████╗░████║██╔══██╗██╔══██╗██╔════╝
#    ███████║██╔████╔██║██║░░██║██████╔╝█████╗░░
#    ██╔══██║██║╚██╔╝██║██║░░██║██╔══██╗██╔══╝░░
#    ██║░░██║██║░╚═╝░██║╚█████╔╝██║░░██║███████╗
#    ╚═╝░░╚═╝╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝
#           
#
#              © Copyright 2022
#
# https://t.me/the_farkhodov | https://t.me/hikariatama
#
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html


# scope: inline
# scope: nini_only
# scope: nino_min 3.2.1

import logging
import git

from telethon.tl.types import Message
from telethon.utils import get_display_name

from .. import loader, main, utils
from ..inline.types import InlineQuery

logger = logging.getLogger(__name__)


@loader.tds
class NinoinfoMod(loader.Module):
    """Show userbot info"""

    strings = {
        "name": "Info",
        "owner": "Владелец",
        "version": "Версия",
        "build": "Сборка",
        "prefix": "Префикс",
        "up-to-date": "🎡 Актуальная версия",
        "update_required": "😕 Требуется обновление</b><code>.update</code><b>",
        "_cfg_cst_msg": "Custom message for info. May contain {me}, {version}, {build}, {prefix}, {platform} keywords",
        "_cfg_cst_btn": "Custom button for info. Leave empty to remove button",
        "_cfg_cst_bnr": "Custom Banner for info.",
        "_cfg_cst_frmt": "Custom fileformat for Banner info.",
        "_cfg_banner": "Set `True` in order to disable an image banner",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                "no",
                doc=lambda: self.strings("_cfg_cst_msg"),
            ),
            loader.ConfigValue(
                "custom_button1",
                ["🦊 Meta", "https://t.me/the_farkhodov"],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button2",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button3",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_banner",
                "https://github.com/NinoZOOM/assets/raw/main/Nino-Banner-Premium%20L.png",
                lambda: self.strings("_cfg_cst_bnr"),
            ),
            loader.ConfigValue(
                "disable_banner",
                False,
                lambda: self.strings("_cfg_banner"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "custom_format",
                "photo",
                lambda: self.strings("_cfg_cst_frmt"),
                validator=loader.validators.Choice(["photo", "video", "gif"]),
            ),
        )

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me()

    def _render_info(self) -> str:
        ver = utils.get_git_hash() or "Unknown"

        try:
            repo = git.Repo()
            diff = repo.git.log(["HEAD..origin/master", "--oneline"])
            upd = (
                self.strings("update_required") if diff else self.strings("up-to-date")
            )
        except Exception:
            upd = ""

        me = f'<b><a href="tg://user?id={self._me.id}">{utils.escape_html(get_display_name(self._me))}</a></b>'
        version = f'<i>{".".join(list(map(str, list(main.__version__))))}</i>'
        build = f'<a href="https://github.com/hikariatama/Hikka/commit/{ver}">#{ver[:8]}</a>'  # fmt: skip
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"
        platform = utils.get_named_platform()

        return (
            "<b> </b>\n"
            + self.config["custom_message"].format(
                me=me,
                version=version,
                build=build,
                prefix=prefix,
                platform=platform,
            )
            if self.config["custom_message"] != "no"
            else (
                "<b>💢 Nino Userbot </b>\n"
                f'<b>🧑‍💻 {self.strings("owner")}: </b>{me}\n\n'
                f"<b>🛰 {self.strings('version')}: </b>{version} {build}\n"
                f"<b>{upd}</b>\n\n"
                f"<b>🎷 {self.strings('prefix')}: </b>{prefix}\n"
                f"<b>📻 Платформа: «{platform}»</b>\n"
                f"<b>🎗 Improve your self value</b>\n"
            )
        )

    def _get_mark(self, int):
        if int == 1:
            return (
                {
                    "text": self.config["custom_button1"][0],
                    "url": self.config["custom_button1"][1],
                }
                if self.config["custom_button1"]
                else None
            )

        elif int == 2:
            return (
                {
                    "text": self.config["custom_button2"][0],
                    "url": self.config["custom_button2"][1],
                }
                if self.config["custom_button2"]
                else None
            )

        elif int == 3:
            return (
                {
                    "text": self.config["custom_button3"][0],
                    "url": self.config["custom_button3"][1],
                }
                if self.config["custom_button3"]
                else None
            )
            
        elif int == 4:
            return (
                {
                    "text": "🔻Close",
                    "action": "close",
                }
            )

    @loader.unrestricted
    async def infocmd(self, message: Message):
        """Send userbot info"""
        m1 = self._get_mark(1)
        m2 = self._get_mark(2)
        m3 = self._get_mark(3)
        m3 = self._get_mark(4)
        await self.inline.form(
            message=message,
            text=self._render_info(),
            reply_markup=[
                [
                    *([m1] if m1 else []),
                ],
                [
                    *([m2] if m2 else []),
                    *([m3] if m3 else []),
                ],
            ],
            **{}
            if self.config["disable_banner"]
            else {self.config["custom_format"]: self.config["custom_banner"]}
        )
