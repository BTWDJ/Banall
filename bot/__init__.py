import asyncio
import logging
import os
from datetime import datetime, timezone
import ntplib
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import *
from .config import Config

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Function to get current time from an NTP server
async def get_ntp_time():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        current_time = datetime.utcfromtimestamp(response.tx_time).replace(tzinfo=timezone.utc)
        logging.debug(f"Fetched NTP time: {current_time.isoformat()}")
        return current_time
    except Exception as e:
        logging.error(f"Failed to fetch NTP time: {e}")
        return datetime.now(timezone.utc)

# Log the fetched NTP time
async def log_ntp_time():
    current_time = await get_ntp_time()
    logging.debug(f"Current system time: {current_time.isoformat()}")

# Define the absolute path for the session storage
session_path = os.path.abspath(os.path.join(os.getcwd(), "sessions"))

# Ensure the session directory exists
if not os.path.exists(session_path):
    os.makedirs(session_path)

async def main():
    await log_ntp_time()

    # Initialize Client with a string identifier and session storage path for Pyrogram v2
    if Config.PYRO_SESSION:
        ass = Client(
            "ass",
            api_id=Config.TELEGRAM_APP_ID,
            api_hash=Config.TELEGRAM_APP_HASH,
            session_string=Config.PYRO_SESSION,
            workdir=session_path
        )

    if Config.TELEGRAM_TOKEN:
        bot_client = Client(
            "bot_client",
            api_id=Config.TELEGRAM_APP_ID,
            api_hash=Config.TELEGRAM_APP_HASH,
            bot_token=Config.TELEGRAM_TOKEN,
            workdir=session_path
        )

    # Rest of your bot code
    if Config.PYRO_SESSION:
        @ass.on_message(filters.command("banall"))
        async def banall(client, message):
            print(f"Getting members from {message.chat.id}")
            async for member in client.get_chat_members(message.chat.id):
                try:
                    await client.ban_chat_member(chat_id=message.chat.id, user_id=member.user.id)
                    print(f"Kicked {member.user.id} from {message.chat.id}")
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    print(e)
                except Exception as e:
                    print(f"Failed to kick {member.user.id} from {message.chat.id}: {e}")
            print("Process completed")

        @ass.on_message(filters.command("mbanall"))
        async def mbanall(client, message):
            print(f"Getting members from {message.chat.id}")
            async for member in client.get_chat_members(message.chat.id):
                try:
                    await client.send_message(message.chat.id, f"/ban {member.user.id}")
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    print(e)
                except Exception as e:
                    print(f"Failed to kick {member.user.id}: {e}")
            print("Process completed")

        @ass.on_message(filters.command(["start", "ping"]))
        async def start(client, message):
            await message.reply_text("Hello, this is banall bot. I can ban members within a second! Just promote me as an admin with ban rights.")

    if Config.TELEGRAM_TOKEN:
        @bot_client.on_message(filters.command("banall"))
        async def banall(client, message):
            print(f"Getting members from {message.chat.id}")
            async for member in client.get_chat_members(message.chat.id):
                try:
                    await client.ban_chat_member(chat_id=message.chat.id, user_id=member.user.id)
                    print(f"Kicked {member.user.id} from {message.chat.id}")
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    print(e)
                except Exception as e:
                    print(f"Failed to kick {member.user.id} from {message.chat.id}: {e}")
            print("Process completed")

        @bot_client.on_message(filters.command("mbanall"))
        async def mbanall(client, message):
            print(f"Getting members from {message.chat.id}")
            async for member in client.get_chat_members(message.chat.id):
                try:
                    await client.send_message(message.chat.id, f"/ban {member.user.id}")
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    print(e)
                except Exception as e:
                    print(f"Failed to kick {member.user.id}: {e}")
            print("Process completed")

        @bot_client.on_message(filters.command(["start", "ping"]))
        async def start(client, message):
            await message.reply_photo(
                photo='https://te.legra.ph/file/c8c39cb8dd2be4068f498.jpg',
                caption="""
                All commands can only be used in groups

                ⨷ /banall : Ban-all members in a group

                ⨷ /unbanall : Unban all members in a group

                ⨷ /kickall : Kick all members in a group

                ⨷ /muteall : Mute all members in a group

                ⨷ /unmuteall : Unmute all members in a group (still will the list in restricted members but all restrictions will go)

                ⨷ /unpinall : Unpin all messages in a group.

                Created by: [DJ](https://t.me/maybeback)
                """
            )

    # Start the clients
    if Config.PYRO_SESSION:
        await ass.start()

    if Config.TELEGRAM_TOKEN:
        await bot_client.start()

    # Keep the clients running
    if Config.PYRO_SESSION:
        await ass.idle()

    if Config.TELEGRAM_TOKEN:
        await bot_client.idle()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
    
