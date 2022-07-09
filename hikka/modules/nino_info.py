# scope: inline

import logging
import git

from telethon.tl.types import Message
from telethon.utils import get_display_name

from .. import loader, main, utils

logger = logging.getLogger(__name__)


@loader.tds
class NinoInfoMod(loader.Module):
    """Show userbot info"""

    strings = {
        "name": "NinoInfo",
        "owner": "Owner",
        "version": "Version",
        "build": "Build",
        "prefix": "Prefix",
        "up-to-date": "▪️ Up-to-date",
        "update_required": "😕 Update required </b><code>.update</code><b>",
        "_cfg_cst_msg": "Custom message for info. May contain {me}, {version}, {build}, {prefix}, {platform}, {upd} keywords",
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
                validator=loader.validators.Choice(["photo", "video", "audio", "gif"]),
            ),
            loader.ConfigValue(
                "custom_button1",
                ["🧑‍💻Meta","https://t.me/the_farkhodov"],
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
                "custom_button4",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button5",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button6",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button7",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button8",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button9",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button10",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button11",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
            ),
            loader.ConfigValue(
                "custom_button12",
                [],
                lambda: self.strings("_cfg_cst_btn"),
                validator=loader.validators.Series(min_len=0, max_len=2),
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
        build = f'<a href="https://github.com/NinoZOOM/Nino/commit/{ver}">#{ver[:8]}</a>'  # fmt: skip
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"
        platform = utils.get_named_platform()

        return (
            self.config["custom_message"].format(
                me=me,
                version=version,
                build=build,
                prefix=prefix,
                platform=platform,
                upd=upd,
            )
            if self.config["custom_message"] != "no"
            else (
                "<b>🧑‍🎤 Nino Premium</b>\n"
                f'<b>▪️ {self.strings("owner")}: </b>{me}\n\n'
                f"<b>▪️ {self.strings('version')}: </b>{version} {build}\n"
                f"<b>{upd}</b>\n\n"
                f"<b>▪️ {self.strings('prefix')}: </b>{prefix}\n"
                f"<b>▪️ Platform: {platform}</b>\n"
            )
        )

    def _get_mark(self, btn_count):
        btn_count = str(btn_count)
        return (
            {
                "text": self.config[f"custom_button{btn_count}"][0],
                "url": self.config[f"custom_button{btn_count}"][1],
            }
            if self.config[f"custom_button{btn_count}"]
            else None
        )

    @loader.unrestricted
    async def infocmd(self, message: Message):
        """Send userbot info"""
        m = {x: self._get_mark(x) for x in range(13)}
        await self.inline.form(
            message=message,
            text=self._render_info(),
            reply_markup=[
                [
                    *([m[1]] if m[1] else []),
                    *([m[2]] if m[2] else []),
                    *([m[3]] if m[3] else []),
                ],
                [
                    *([m[4]] if m[4] else []),
                    *([m[5]] if m[5] else []),
                    *([m[6]] if m[6] else []),
                ],
                [
                    *([m[7]] if m[7] else []),
                    *([m[8]] if m[8] else []),
                    *([m[9]] if m[9] else []),
                ],
                [
                    *([m[10]] if m[10] else []),
                    *([m[11]] if m[11] else []),
                    *([m[12]] if m[12] else []),
                ],
            ],
            **{}
            if self.config["disable_banner"]
            else {self.config["custom_format"]: self.config["custom_banner"]},
        )
