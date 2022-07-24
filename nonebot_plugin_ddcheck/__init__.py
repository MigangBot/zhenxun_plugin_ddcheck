import traceback
from loguru import logger
from nonebot.params import CommandArg
from nonebot import on_command, require
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from services.log import logger

require("nonebot_plugin_apscheduler")

from .data_source import get_reply

__plugin_meta__ = PluginMetadata(
    name="成分姬",
    description="查询B站用户关注的VTuber成分",
    usage="查成分 B站用户名/UID",
    extra={
        "unique_name": "ddcheck",
        "example": "查成分 小南莓Official",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.1.11",
    },
)

__zx_plugin_name__ = "成分姬"
__plugin_usage__ = """
usage：
    指令：
        查成分 [用户名/UID]
    示例：
        查成分 少年Pi
""".strip()
__plugin_des__ = "成分姬"
__plugin_type__ = ("好玩的",)
__plugin_version__ = 0.4
__plugin_cmd__ = ["查成分 [用户名/UID]"]
__plugin_author__ = "meetwq"

__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": [],
}
__plugin_configs__ = {
    "BILIBILI_COOKIE": {
        "value": "",
        "help": "若要显示主播牌子，需添加B站用户cookie",
        "default_value": "",
    }
}

ddcheck = on_command("查成分", block=True, priority=12)


@ddcheck.handle()
async def _(msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if not text:
        await ddcheck.finish()

    try:
        res = await get_reply(text)
    except:
        logger.warning(traceback.format_exc())
        await ddcheck.finish("出错了，请稍后再试")

    if isinstance(res, str):
        await ddcheck.finish(res)
    else:
        await ddcheck.finish(MessageSegment.image(res))
