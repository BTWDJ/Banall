import asyncio
import logging
import os
from datetime import datetime
import ntplib
from time import ctime
from pyrogram import Client, filters
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import *
from .config import Config
from pyrogram.errors import ChatAdminRequired

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Function to synchronize time
def sync_time():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        os.environ['TZ'] = 'UTC'
        os.system('export TZ=UTC')
        os.system('date %s' % response.tx_time)
        logging.debug(f"Time synchronized to: {ctime(response.tx_time)}")
    except Exception as e:
        logging.error(f"Failed to synchronize time: {e}")

# Synchronize time at startup
sync_time()

# Define the absolute path for the session storage
session_path = os.path.abspath(os.path.join(os.getcwd(), "sessions"))

# Ensure the session directory exists
if not os.path.exists(session_path):
    os.makedirs(session_path)

# Initialize Client with a string identifier and session storage path for Pyrogram v1
if Config.PYRO_SESSION:
    ass = Client(
        session_name="ass",
        api_id=Config.TELEGRAM_APP_ID,
        api_hash=Config.TELEGRAM_APP_HASH,
        workdir=session_path
    )

if Config.TELEGRAM_TOKEN:
    bot = Client(
        session_name=":memory:",
        api_id=Config.TELEGRAM_APP_ID,
        api_hash=Config.TELEGRAM_APP_HASH,
        bot_token=Config.TELEGRAM_TOKEN,
        workdir=session_path
    )

# Rest of your bot code
if Config.PYRO_SESSION:
    @ass.on_message(filters.command("banall"))
    async def _(bot, msg):
        print("getting members from {}".format(msg.chat.id))
        async for i in bot.iter_chat_members(msg.chat.id):
            try:
                await bot.ban_chat_member(chat_id=msg.chat.id, user_id=i.user.id)
                print("kicked {} from {}".format(i.user.id, msg.chat.id))
            except FloodWait as e:
                await asyncio.sleep(e.x)
                print(e)
            except Exception as e:
                print("failed to kick {} from {}".format(i.user.id, e))
        print("process completed")

    @ass.on_message(filters.command("mbanall"))
    async def mban(bot, msg):
        print("getting members from {}".format(msg.chat.id))
        async for i in bot.iter_chat_members(msg.chat.id):
            try:
                await bot.send_message(msg.chat.id, f"/ban {i.user.id}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
                print(e)
            except Exception as e:
                print("failed to kick {} from {}".format(i.user.id, e))
        print("process completed")

    @ass.on_message(filters.command(["start", "ping"]))
    async def hello(bot, message):
        await message.reply("Hello, this is banall bot. I can ban members within a second! Just promote me as an admin with ban rights.")

if Config.TELEGRAM_TOKEN:
    @bot.on_message(filters.command("banall"))
    async def _(bot, msg):
        print("getting members from {}".format(msg.chat.id))
        async for i in bot.iter_chat_members(msg.chat.id):
            try:
                await bot.ban_chat_member(chat_id=msg.chat.id, user_id=i.user.id)
                print("kicked {} from {}".format(i.user.id, msg.chat.id))
            except FloodWait as e:
                await asyncio.sleep(e.x)
                print(e)
            except Exception as e:
                print("failed to kick {} from {}".format(i.user.id, e))
        print("process completed")

    @bot.on_message(filters.command("mbanall"))
    async def mban(bot, msg):
        print("getting members from {}".format(msg.chat.id))
        async for i in bot.iter_chat_members(msg.chat.id):
            try:
                await bot.send_message(msg.chat.id, f"/ban {i.user.id}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
                print(e)
            except Exception as e:
                print("failed to kick {} from {}".format(i.user.id, e))
        print("process completed")

    @bot.on_message(filters.command(["start", "ping"]))
    async def hello(bot, message):
        await message.reply_photo(photo='https://te.legra.ph/file/c8c39cb8dd2be4068f498.jpg', caption="""
    All commands can only be used in groups

⨷ /banall : Ban-all members in a group

⨷ /unbanall : Unban all members in a group

⨷ /kickall : Kick all members in a group

⨷ /muteall : Mute all members in a group

⨷ /unmuteall : Unmute all members in a group (still will the list in restricted members but all restrictions will go)

⨷ /unpinall : Unpin all messages in a group.

Created by: [DJ](https://t.me/maybeback)
""")
        
