# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT


from random import randint
from typing import Optional

from contextlib import suppress
from pyrogram import Client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from . import *


daftar_join = []

turun_dewek = False


__MODULE__ = "Voice Chat"
__HELP__ = f"""
Bantuan Untuk Voice Chat


• Perintah: <code>{cobadah}startvc</code>
• Penjelasan: Untuk memulai voice chat grup.

• Perintah: <code>{cobadah}stopvc</code>
• Penjelasan: Untuk mengakhiri voice chat grup.

• Perintah: <code>{cobadah}joinvc</code>
• Penjelasan: Untuk bergabung voice chat grup.

• Perintah: <code>{cobadah}leavevc</code>
• Penjelasan: Untuk meninggalkan voice chat grup.


 © {bot.me.first_name.split()[0]}
"""


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await eor(message, f"**No group call Found** {err_msg}")
    return False


@ubot.on_message(filters.command(["startvcs"], "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(anjay(["startvc"]) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    ky = await eor(message, "<code>Processing....</code>")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = (
        f"<b>Obrolan Suara Aktif</b>\n • <b>Chat :</b><code>{message.chat.title}</code>"
    )
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • <b>Title :</b> <code>{vctitle}</code>"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await ky.edit(args)
    except Exception as e:
        await ky.edit(f"<b>INFO:</b> `{e}`")


@ubot.on_message(filters.command(["stopvcs"], "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(anjay(["stopvc"]) & filters.me)
async def end_vc_(client: Client, message: Message):
    ky = await eor(message, "<code>Processing....</code>")
    message.chat.id
    if not (
        group_call := (await get_group_call(client, message, err_msg=", Kesalahan..."))
    ):
        return
    await client.send(DiscardGroupCall(call=group_call))
    await ky.edit(
        f"<b>Obrolan Suara Diakhiri</b>\n • <b>Chat :</b><code>{message.chat.title}</code>"
    )

@ubot.on_message(filters.command(["joinvcs"], "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(anjay(["joinvc"]) & filters.me)
async def joinvc(client, message):
    if message.from_user.id != client.me.id:
        ky = await message.reply("<code>Processing....</code>")
    else:
        ky = await eor(message, "<code>Processing....</code>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.vc.start(chat_id)

    except Exception as e:
        return await ky.edit(f"ERROR: {e}")
    await ky.edit(
        f"❏ <b>Berhasil Join Voice Chat</b>\n└ <b>Chat :</b><code>{message.chat.title}</code>"
    )
    await sleep(1)
    await client.vc.set_is_mute(True)
    
    await ky.delete()


@ubot.on_message(filters.command(["leavevcs"], "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(anjay(["leavevc"]) & filters.me)
async def leavevc(client, message):
    global turun_dewek
    if message.from_user.id != client.me.id:
        ky = await message.reply("<code>Processing....</code>")
    else:
        ky = await eor(message, "<code>Processing....</code>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
      
        await client.vc.stop()

    except Exception as e:
        return await ky.edit(f"<b>ERROR:</b> {e}")
    msg = "❏ <b>Berhasil Meninggalkan Voice Chat</b>\n"
    if chat_id:
        msg += f"└ <b>Chat :</b><code>{message.chat.title}</code>"
    await ky.edit(msg)
    await sleep(1)
    await ky.delete()
