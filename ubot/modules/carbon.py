# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT

import asyncio

from pyrogram import *
from pyrogram.types import *

from . import bot, ubot, anjay, cobadah
from ubot.config import PREFIX
from ubot.utils import *

__MODULE__ = "Carbon"
__HELP__ = f"""
Bantuan Untuk Carbon


• Perintah: <code>{cobadah}carbon</code> [balas pesan]
• Penjelasan: Untuk membuat teks menjadi carbonara.


© {bot.me.first_name.split()[0]}
"""


@ubot.on_message(filters.me & anjay(["carbon"]))
async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await eor(message, "Processing . . .")
    carbon = await make_carbon(text)
    await ex.edit("Uploading . . .")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"<b>Carbonised by :</b>{client.me.mention}",
        ),
    )
    carbon.close()
