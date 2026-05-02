import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

# 🛑 1. APNA BOT TOKEN YAHAN DALEIN
TOKEN = "7685935373:AAFpgKZEMY5aiYihtAJ0mzZslTK8Wjp3PlY"

# 💎 2. FORCE JOIN CHANNELS (Yahan apne 4 channels ke username dalein bina link ke, sirf @ lagayen)
CHANNELS = [
    "@USMANOTPCHANNEL",     # Channel 1
    "@shadowinnovations",         # Channel 2
    "@USMANSARKARBIO",    # Channel 3 (Change karein)
    "@USMANSARKARCHATGROUP"     # Channel 4 (Change karein)
]

dp = Dispatcher()

# ==========================================
# 🛡️ FORCE JOIN CHECKER SYSTEM
# ==========================================
async def check_all_channels(user_id: int, bot: Bot) -> bool:
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            # Agar bot channel me admin nahi hoga toh false return karega
            print(f"Error checking channel {channel}: {e}")
            return False
    return True

def get_force_join_keyboard():
    builder = InlineKeyboardBuilder()
    # 4 channels ke liye 4 buttons
    for i, channel in enumerate(CHANNELS, 1):
        builder.button(text=f"🔗 Join Channel {i}", url=f"https://t.me/{channel.replace('@', '')}")
    
    # Buttons ko 1 column me set karega (niche upar)
    builder.adjust(1)
    return builder.as_markup()

# ==========================================
# 🎁 EXTREME PREMIUM WELCOME MESSAGE
# ==========================================
@dp.message(CommandStart())
async def send_welcome(message: types.Message, bot: Bot):
    # 1. Check Force Join
    is_joined = await check_all_channels(message.from_user.id, bot)
    
    if not is_joined:
        access_text = (
            "⚠️ <b>ACCESS DENIED</b> ⚠️\n\n"
            "<i>Apko Bot Use Karny K Liye Hamary 4 Official Channels Join Karny HongY. "
            "Niche diye gaye buttons par click karein aur join karne ke baad wapis /start bhejen.</i>"
        )
        await message.answer(access_text, parse_mode=ParseMode.HTML, reply_markup=get_force_join_keyboard())
        return

    # 2. Premium Welcome Text
    start_text = (
        "╔══════════════════════════╗\n"
        "║ 💎 <b>PREMIUM MODE ACTIVE</b> 💎 ║\n"
        "╚══════════════════════════╝\n\n"
        "🌟 <b>Account Status:</b> <code>EXTREME ACCESS</code>\n"
        "🎟 <b>Tokens Required:</b> <code>0 (Enjoy!)</code>\n\n"
        '<tg-emoji emoji-id="5420315771991497307">🔥</tg-emoji> <i>Admin has enabled Premium Mode! Send any Mobile Number or CNIC to extract details instantly without limits.</i>\n\n'
        "<i>DEVELOPED BY USMAN SARKAR</i>"
    )
    
    await message.answer(start_text, parse_mode=ParseMode.HTML)


# ==========================================
# ⚡ NUMBER FETCHING & EXTREME UI RESULT
# ==========================================
@dp.message(F.text)
async def fetch_sim_info(message: types.Message, bot: Bot):
    # Pehle phir se check karein ke user ne channel leave toh nahi kar diya
    is_joined = await check_all_channels(message.from_user.id, bot)
    if not is_joined:
        await message.answer("⚠️ <b>ACCESS REVOKED:</b> <i>Aapne channels leave kar diye hain. Pehle join karein! /start</i>", parse_mode=ParseMode.HTML)
        return

    query = message.text.strip()
    
    # 1. SEND PREMIUM LOADING TEXT
    loading_text = '🔘 <i>Extracting from Premium Database... Please wait</i>'
    loading_msg = await message.answer(loading_text, parse_mode=ParseMode.HTML)

    # Thora wait taake loading UI feel ho
    await asyncio.sleep(1.5)

    # API Endpoint
    url = f"https://sim-info-api.wasif-ali.workers.dev/?search={query}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                
                # 2. DELETE LOADING MESSAGE
                if loading_msg:
                    try:
                        await loading_msg.delete()
                    except Exception: 
                        pass
                
                # 3. HANDLE API RESPONSE
                if response.status == 200:
                    data = await response.json()
                    
                    if not data:
                        await message.answer("❌ <b>NO RECORD FOUND</b>\n<i>Database mein ye number majood nahi hai.</i>", parse_mode=ParseMode.HTML)
                        return
                    
                    # 4. EXTREME PRO RESULT FORMATTING (Same as your screenshot)
                    # Data ko string banayenge taake format list/dict jaisa hi dikhe
                    data_str = str(data).replace("'", '"') 
                    
                    result_text = "👑 <b>𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐒𝐈𝐌 𝐈𝐍𝐅𝐎</b> 👑\n"
                    result_text += "━━━━━━━━━━━━━━━━━━━━━━\n"
                    result_text += "🔹 <b>Success:</b> <code>True</code>\n"
                    result_text += "🔹 <b>Count:</b> <code>1</code>\n"
                    result_text += f"🔹 <b>Data:</b> <code>{data_str}</code>\n"
                    result_text += "🔹 <b>Developer:</b> <code>USMAN SARKAR👑</code>\n"
                    result_text += "🔹 <b>Telegram:</b> @usmansarkarcyber\n"
                    result_text += "🔹 <b>Channel:</b> @USMANSARKARBIO\n"
                    result_text += "━━━━━━━━━━━━━━━━━━━━━━\n"
                    result_text += "✨ <i>Data Extracted Successfully</i> ✨"
                    
                    await message.answer(result_text, parse_mode=ParseMode.HTML)
                    
                else:
                    await message.answer(f"⚠️ <b>Server Error:</b> <code>{response.status}</code>", parse_mode=ParseMode.HTML)
                    
        except Exception as e:
            if loading_msg:
                try:
                    await loading_msg.delete()
                except Exception: 
                    pass
            await message.answer(f"🚨 <b>System Error:</b> <code>{str(e)}</code>", parse_mode=ParseMode.HTML)

# Run Bot
async def main():
    bot = Bot(token=TOKEN)
    print("🚀 Extreme Premium Bot with 4x Force Join is Online!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
