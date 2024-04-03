from datetime import datetime
import os
from MukeshRobot.modules.disable import DisableAbleCommandHandler
from MukeshRobot import dispatcher
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)

from MukeshRobot import pbot as app
ENV = bool(os.environ.get("ENV", True))
OWNER_ID = 6529892817
OWNER_USERNAME = "obito_shadow"
LOG_CHANNEL = -1002073359557

from MukeshRobot.utils.errors import capture_err


def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@app.on_message(filters.command("request"))
@capture_err
async def reqgban(_, msg: Message):
    if msg.chat.username:
        chat_username = (f"@{msg.chat.username} / `{msg.chat.id}`")
    else:
        chat_username = (f"Private Group / `{msg.chat.id}`")

    bugs = content(msg)
    user_id = msg.from_user.id
    mention = "["+msg.from_user.first_name+"](tg://user?id="+str(msg.from_user.id)+")"
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    thumb = "https://graph.org/file/176e23c720b9dcd270682.jpg"
    
    bug_report = f"""
**ᴀɴɪᴍᴇ ʀᴇǫᴜᴇsᴛ : ** **@{OWNER_USERNAME}**
**ғʀᴏᴍ ᴜsᴇʀ : ** **{mention}**
**ᴜsᴇʀ ɪᴅ : ** **{user_id}**
**ɢʀᴏᴜᴘ : ** **{chat_username}**
**ᴀɴɪᴍᴇ ɴᴀᴍᴇ : ** **{bugs}**
**ᴇᴠᴇɴᴛ sᴛᴀᴍᴘ : ** **{datetimes}**"""

    
    if msg.chat.type == "private":
        await msg.reply_text("<b>This command only works in groups.</b>")
        return

    if user_id == OWNER_ID:
        if bugs:
            await msg.reply_text(
                "<b>How can be bot owner requesting gban??</b>",
            )
            return
        else:
            await msg.reply_text(
                "No Useless Gbans!"
            )
    elif user_id != OWNER_ID:
        if bugs:
            await msg.reply_text(
                f"<b>ᴀɴɪᴍᴇ ʀᴇǫᴜᴇsᴛ : {bugs}</b>\n\n"
                "<b>ᴛʜᴇ ᴀɴɪᴍᴇ ᴡᴀs sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛᴏ ᴛʜᴇ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ.</b>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Close", callback_data=f"close_reply")
                        ]
                    ]
                )
            )
            await app.send_photo(
                LOG_CHANNEL,
                photo=thumb,
                caption=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "", url=f"{msg.link}")
                        ],
                        [
                            InlineKeyboardButton(
                                "Close", callback_data="close_send_photo")
                        ]
                    ]
                )
            )
        else:
            await msg.reply_text(
                f"<b>ɴᴏ ᴀɴɪᴍᴇ ᴛᴏ ʀᴇǫᴜᴇsᴛ.</b>",
            )
        

@app.on_callback_query(filters.regex("close_reply"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()

@app.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_, CallbackQuery):
    is_Admin = await Client.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not is_Admin.can_delete_messages:
        return await CallbackQuery.answer(
            "You're not allowed to close this.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()

__help__ = """
» /reqgban : ʏᴏᴜ ᴄᴀɴ ʀᴇǫᴜᴇsᴛ ᴜs ᴛᴏ ɢʙᴀɴ.
"""

__mod_name__ = "Rᴇǫɢʙᴀɴ"
REQGBAN_HANDLER = DisableAbleCommandHandler("reqgban", reqgban, run_async=True)

dispatcher.add_handler(REQGBAN_HANDLER)
