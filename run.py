# import os
# import asyncio
# import json
# from datetime import datetime, timedelta
# from aiogram import Bot, Dispatcher, F
# from aiogram.filters import Command
# from aiogram.types import Message, FSInputFile, ChatPermissions, InputMediaPhoto, CallbackQuery
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage

# # CONFIG
# BOT_TOKEN = os.getenv("BOT_TOKEN", "your token")
# ADMIN_ID = int(os.getenv("ADMIN_ID", "your id"))

# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(storage=MemoryStorage())

# DATA_FILE = "channels.json"
# LOG_FILE = "logs.txt"

# # DATABASE
# def load_data():
#     try:
#         if os.path.exists(DATA_FILE):
#             with open(DATA_FILE, "r", encoding="utf-8") as f:
#                 return {int(k): v for k, v in json.load(f).items()}
#         return {}
#     except:
#         return {}

# def save_data(data):
#     try:
#         with open(DATA_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#     except:
#         pass

# user_channels = load_data()

# # STATES
# class ChannelStates(StatesGroup):
#     waiting_for_channel_id = State()
#     waiting_for_new_title = State()
#     waiting_for_new_description = State()
#     waiting_for_message = State()
#     waiting_for_photo = State()
#     waiting_for_media_group = State()
#     waiting_for_poll = State()
#     waiting_for_ban_user = State()
#     waiting_for_unban_user = State()
#     waiting_for_restrict_user = State()
#     waiting_for_promote_user = State()
#     waiting_for_pin_message = State()
#     waiting_for_chat_photo = State()

# # LOG
# def write_log(user_id, username, action, details=""):
#     try:
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         with open(LOG_FILE, "a", encoding="utf-8") as f:
#             f.write(f"[{timestamp}] {user_id} (@{username}) | {action} | {details}\n")
#         asyncio.create_task(bot.send_message(ADMIN_ID, f"📋 {action}\n👤 {user_id}\n{details[:50]}"))
#     except:
#         pass

# # KEYBOARDS
# def get_main_menu():
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel")],
#         [InlineKeyboardButton(text="📊 Kanallarim", callback_data="my_channels")],
#         [InlineKeyboardButton(text="❓ Yordam", callback_data="help")]
#     ])

# def get_channel_list(user_id):
#     kb = []
#     if user_id in user_channels and user_channels[user_id]:
#         for idx, ch in enumerate(user_channels[user_id]):
#             emoji = "📢" if ch["type"] == "channel" else "👥"
#             kb.append([InlineKeyboardButton(text=f"{emoji} {ch['name'][:25]}", callback_data=f"sel_{idx}")])
#     kb.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="main")])
#     return InlineKeyboardMarkup(inline_keyboard=kb)

# def get_channel_menu(idx):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="📊 Ma'lumot", callback_data=f"info_{idx}"),
#          InlineKeyboardButton(text="📤 Xabar", callback_data=f"send_{idx}")],
#         [InlineKeyboardButton(text="✏️ Nom", callback_data=f"title_{idx}"),
#          InlineKeyboardButton(text="📝 Tavsif", callback_data=f"desc_{idx}")],
#         [InlineKeyboardButton(text="🖼 Rasm", callback_data=f"pic_{idx}"),
#          InlineKeyboardButton(text="📌 Pin", callback_data=f"pin_{idx}")],
#         [InlineKeyboardButton(text="👥 A'zolar", callback_data=f"mem_{idx}"),
#          InlineKeyboardButton(text="🔗 Havola", callback_data=f"link_{idx}")],
#         [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"del_{idx}")],
#         [InlineKeyboardButton(text="🔙 Orqaga", callback_data="my_channels")]
#     ])

# def get_send_menu(idx):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="💬 Matn", callback_data=f"txt_{idx}"),
#          InlineKeyboardButton(text="📸 Rasm", callback_data=f"pho_{idx}")],
#         [InlineKeyboardButton(text="🖼 Media", callback_data=f"med_{idx}"),
#          InlineKeyboardButton(text="📊 Poll", callback_data=f"pol_{idx}")],
#         [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
#     ])

# def get_member_menu(idx):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="🚫 Ban", callback_data=f"ban_{idx}"),
#          InlineKeyboardButton(text="✅ Unban", callback_data=f"unb_{idx}")],
#         [InlineKeyboardButton(text="⚠️ Restrict", callback_data=f"res_{idx}"),
#          InlineKeyboardButton(text="⭐️ Promote", callback_data=f"pro_{idx}")],
#         [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
#     ])

# def get_pin_menu(idx):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="📌 Pin", callback_data=f"dopin_{idx}"),
#          InlineKeyboardButton(text="📍 Unpin", callback_data=f"unpin_{idx}")],
#         [InlineKeyboardButton(text="🚫 Unpin All", callback_data=f"unpinall_{idx}")],
#         [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
#     ])

# def get_pic_menu(idx):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="🖼 O'rnatish", callback_data=f"setpic_{idx}"),
#          InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"delpic_{idx}")],
#         [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
#     ])

# def get_link_menu(idx):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="🔗 Doimiy", callback_data=f"explink_{idx}"),
#          InlineKeyboardButton(text="⏰ Cheklangan", callback_data=f"crtlink_{idx}")],
#         [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
#     ])

# # START
# @dp.message(Command("start"))
# async def start_cmd(msg: Message):
#     write_log(msg.from_user.id, msg.from_user.username or "noname", "START", "")
#     await msg.answer("🤖 <b>Telegram Kanal Bot</b>\n\nKanallaringizni boshqaring!", parse_mode="HTML", reply_markup=get_main_menu())

# @dp.callback_query(F.data == "main")
# async def main_cb(cb: CallbackQuery):
#     await cb.message.edit_text("🤖 <b>Asosiy menyu</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     await cb.answer()

# @dp.callback_query(F.data == "help")
# async def help_cb(cb: CallbackQuery):
#     await cb.message.edit_text("❓ <b>YORDAM</b>\n\n1. Kanal qo'shing\n2. Bot admin qiling\n3. Boshqaring!\n\n<b>Admin:</b> /stats /logs /backup", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="main")]]))
#     await cb.answer()

# # ADD CHANNEL
# @dp.callback_query(F.data == "add_channel")
# async def add_ch_cb(cb: CallbackQuery, state: FSMContext):
#     await cb.message.edit_text("📝 <b>Kanal ID/username:</b>\n\n<code>-1001234567890</code>\n<code>@channel</code>", parse_mode="HTML")
#     await state.set_state(ChannelStates.waiting_for_channel_id)
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_channel_id)
# async def add_ch_proc(msg: Message, state: FSMContext):
#     ch_id = msg.text.strip()
#     try:
#         chat = await bot.get_chat(chat_id=ch_id)
#         bot_mem = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
#         if bot_mem.status not in ["administrator", "creator"]:
#             await msg.answer("❌ Bot admin emas!", reply_markup=get_main_menu())
#             await state.clear()
#             return
        
#         uid = msg.from_user.id
#         if uid not in user_channels:
#             user_channels[uid] = []
        
#         if any(c["id"] == chat.id for c in user_channels[uid]):
#             await msg.answer("⚠️ Allaqachon qo'shilgan!", reply_markup=get_main_menu())
#             await state.clear()
#             return
        
#         user_channels[uid].append({"id": chat.id, "username": chat.username, "name": chat.title, "type": chat.type, "added": datetime.now().strftime("%Y-%m-%d %H:%M")})
#         save_data(user_channels)
#         write_log(uid, msg.from_user.username or "noname", "ADDED", chat.title)
#         await msg.answer(f"✅ <b>Qo'shildi!</b>\n\n📢 {chat.title}\n🆔 <code>{chat.id}</code>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# # MY CHANNELS
# @dp.callback_query(F.data == "my_channels")
# async def my_ch_cb(cb: CallbackQuery):
#     uid = cb.from_user.id
#     if uid not in user_channels or not user_channels[uid]:
#         await cb.message.edit_text("📭 <b>Kanal yo'q!</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="➕ Qo'shish", callback_data="add_channel")],[InlineKeyboardButton(text="🔙 Orqaga", callback_data="main")]]))
#     else:
#         await cb.message.edit_text(f"📊 <b>Kanallar ({len(user_channels[uid])} ta)</b>", parse_mode="HTML", reply_markup=get_channel_list(uid))
#     await cb.answer()

# @dp.callback_query(F.data.startswith("sel_"))
# async def sel_ch_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     uid = cb.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await cb.answer("❌ Topilmadi!", show_alert=True)
#         return
#     ch = user_channels[uid][idx]
#     emoji = "📢" if ch["type"] == "channel" else "👥"
#     await cb.message.edit_text(f"{emoji} <b>{ch['name']}</b>\n\n🆔 <code>{ch['id']}</code>\n📅 {ch['added']}", parse_mode="HTML", reply_markup=get_channel_menu(idx))
#     await cb.answer()

# @dp.callback_query(F.data.startswith("del_"))
# async def del_ch_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     uid = cb.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await cb.answer("❌ Topilmadi!", show_alert=True)
#         return
#     ch = user_channels[uid].pop(idx)
#     save_data(user_channels)
#     write_log(uid, cb.from_user.username or "noname", "DELETED", ch['name'])
#     await cb.message.edit_text(f"✅ <b>O'chirildi!</b>\n\n📢 {ch['name']}", parse_mode="HTML", reply_markup=get_main_menu())
#     await cb.answer()

# @dp.callback_query(F.data.startswith("info_"))
# async def info_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     uid = cb.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await cb.answer("❌ Topilmadi!", show_alert=True)
#         return
#     ch = user_channels[uid][idx]
#     try:
#         chat = await bot.get_chat(chat_id=ch["id"])
#         count = await bot.get_chat_member_count(chat_id=ch["id"])
#         await cb.message.edit_text(f"📊 <b>Ma'lumot</b>\n\n📝 {chat.title}\n🆔 <code>{chat.id}</code>\n📖 {chat.description or 'Yo`q'}\n👤 @{chat.username or 'Yo`q'}\n👥 {count:,}", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]]))
#     except Exception as e:
#         await cb.answer(f"❌ {str(e)[:50]}", show_alert=True)
#     await cb.answer()

# # TITLE
# @dp.callback_query(F.data.startswith("title_"))
# async def title_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_new_title)
#     await cb.message.edit_text("✏️ <b>Yangi nom:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_new_title)
# async def title_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         await bot.set_chat_title(chat_id=ch["id"], title=msg.text.strip())
#         user_channels[uid][idx]["name"] = msg.text.strip()
#         save_data(user_channels)
#         write_log(uid, msg.from_user.username or "noname", "TITLE", msg.text.strip())
#         await msg.answer("✅ <b>Nom o'zgartirildi!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# # DESCRIPTION
# @dp.callback_query(F.data.startswith("desc_"))
# async def desc_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_new_description)
#     await cb.message.edit_text("📝 <b>Yangi tavsif:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_new_description)
# async def desc_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         await bot.set_chat_description(chat_id=ch["id"], description=msg.text.strip())
#         write_log(uid, msg.from_user.username or "noname", "DESC", ch['name'])
#         await msg.answer("✅ <b>Tavsif o'zgartirildi!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# # SEND MENU
# @dp.callback_query(F.data.startswith("send_"))
# async def send_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     await cb.message.edit_text("📤 <b>Xabar yuborish</b>", parse_mode="HTML", reply_markup=get_send_menu(idx))
#     await cb.answer()

# @dp.callback_query(F.data.startswith("txt_"))
# async def txt_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_message)
#     await cb.message.edit_text("💬 <b>Matn yuboring:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_message)
# async def txt_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         await bot.send_message(chat_id=ch["id"], text=msg.text, parse_mode="HTML")
#         write_log(uid, msg.from_user.username or "noname", "MSG_SENT", ch['name'])
#         await msg.answer("✅ <b>Yuborildi!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# @dp.callback_query(F.data.startswith("pho_"))
# async def pho_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_photo)
#     await cb.message.edit_text("📸 <b>Rasm yuboring:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_photo, F.photo)
# async def pho_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         await bot.send_photo(chat_id=ch["id"], photo=msg.photo[-1].file_id, caption=msg.caption, parse_mode="HTML")
#         write_log(uid, msg.from_user.username or "noname", "PHOTO_SENT", ch['name'])
#         await msg.answer("✅ <b>Yuborildi!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# @dp.callback_query(F.data.startswith("med_"))
# async def med_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx, media=[])
#     await state.set_state(ChannelStates.waiting_for_media_group)
#     await cb.message.edit_text("🖼 <b>Rasmlar yuboring</b>\n\n/done - tugadi", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_media_group, F.photo)
# async def med_collect(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     media = data.get("media", [])
#     media.append({"file_id": msg.photo[-1].file_id, "caption": msg.caption})
#     await state.update_data(media=media)
#     await msg.answer(f"✅ {len(media)} ta\n\n/done")

# @dp.message(ChannelStates.waiting_for_media_group, Command("done"))
# async def med_done(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     media = data.get("media", [])
#     uid = msg.from_user.id
#     if not media or len(media) < 2:
#         await msg.answer("❌ Kamida 2 ta!", reply_markup=get_main_menu())
#         return
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         group = []
#         for i, m in enumerate(media):
#             if i == 0:
#                 group.append(InputMediaPhoto(media=m["file_id"], caption=m["caption"]))
#             else:
#                 group.append(InputMediaPhoto(media=m["file_id"]))
#         await bot.send_media_group(chat_id=ch["id"], media=group)
#         write_log(uid, msg.from_user.username or "noname", "MEDIA_SENT", f"{len(media)} photos")
#         await msg.answer(f"✅ <b>Yuborildi!</b>\n\n🖼 {len(media)} ta", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# @dp.callback_query(F.data.startswith("pol_"))
# async def pol_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_poll)
#     await cb.message.edit_text("📊 <b>Format:</b>\n\nSavol\nVariant1\nVariant2", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_poll)
# async def pol_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     lines = msg.text.strip().split("\n")
#     if len(lines) < 3:
#         await msg.answer("❌ Kamida savol va 2 variant!", reply_markup=get_main_menu())
#         return
#     ch = user_channels[uid][idx]
#     try:
#         await bot.send_poll(chat_id=ch["id"], question=lines[0], options=[l.strip() for l in lines[1:] if l.strip()], is_anonymous=True)
#         write_log(uid, msg.from_user.username or "noname", "POLL_SENT", ch['name'])
#         await msg.answer("✅ <b>Yuborildi!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# # PICTURE
# @dp.callback_query(F.data.startswith("pic_"))
# async def pic_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     await cb.message.edit_text("🖼 <b>Kanal rasmi</b>", parse_mode="HTML", reply_markup=get_pic_menu(idx))
#     await cb.answer()

# @dp.callback_query(F.data.startswith("setpic_"))
# async def setpic_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_chat_photo)
#     await cb.message.edit_text("🖼 <b>Rasm yuboring:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_chat_photo, F.photo)
# async def setpic_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     path = f"temp_{uid}.jpg"
#     try:
#         file = await bot.get_file(msg.photo[-1].file_id)
#         await bot.download_file(file.file_path, path)
#         with open(path, 'rb') as photo:
#             await bot.set_chat_photo(chat_id=ch["id"], photo=photo)
#         if os.path.exists(path):
#             os.remove(path)
#         write_log(uid, msg.from_user.username or "noname", "PIC_SET", ch['name'])
#         await msg.answer("✅ <b>O'rnatildi!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#         if os.path.exists(path):
#             os.remove(path)
#     await state.clear()

# @dp.callback_query(F.data.startswith("delpic_"))
# async def delpic_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     uid = cb.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await cb.answer("❌ Topilmadi!", show_alert=True)
#         return
#     ch = user_channels[uid][idx]
#     try:
#         await bot.delete_chat_photo(chat_id=ch["id"])
#         write_log(uid, cb.from_user.username or "noname", "PIC_DEL", ch['name'])
#         await cb.message.edit_text("✅ <b>O'chirildi!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await cb.answer(f"❌ {str(e)[:50]}", show_alert=True)
#     await cb.answer()

# # PIN
# @dp.callback_query(F.data.startswith("pin_"))
# async def pin_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     await cb.message.edit_text("📌 <b>Pin</b>", parse_mode="HTML", reply_markup=get_pin_menu(idx))
#     await cb.answer()

# @dp.callback_query(F.data.startswith("dopin_"))
# async def dopin_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_pin_message)
#     await cb.message.edit_text("📌 <b>Xabar ID:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_pin_message)
# async def dopin_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         msg_id = int(msg.text.strip())
#         await bot.pin_chat_message(chat_id=ch["id"], message_id=msg_id)
#         write_log(uid, msg.from_user.username or "noname", "PINNED", f"ID: {msg_id}")
#         await msg.answer("✅ <b>Pin qilindi!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except ValueError:
#         await msg.answer("❌ Faqat raqam!", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# @dp.callback_query(F.data.startswith("unpin_"))
# async def unpin_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     uid = cb.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await cb.answer("❌ Topilmadi!", show_alert=True)
#         return
#     ch = user_channels[uid][idx]
#     try:
#         await bot.unpin_chat_message(chat_id=ch["id"])
#         write_log(uid, cb.from_user.username or "noname", "UNPINNED", ch['name'])
#         await cb.message.edit_text("✅ <b>Unpin!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await cb.answer(f"❌ {str(e)[:50]}", show_alert=True)
#     await cb.answer()

# @dp.callback_query(F.data.startswith("unpinall_"))
# async def unpinall_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     uid = cb.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await cb.answer("❌ Topilmadi!", show_alert=True)
#         return
#     ch = user_channels[uid][idx]
#     try:
#         await bot.unpin_all_chat_messages(chat_id=ch["id"])
#         write_log(uid, cb.from_user.username or "noname", "UNPINNED_ALL", ch['name'])
#         await cb.message.edit_text("✅ <b>Hammasi unpin!</b>", parse_mode="HTML", reply_markup=get_main_menu())
#     except Exception as e:
#         await cb.answer(f"❌ {str(e)[:50]}", show_alert=True)
#     await cb.answer()

# # MEMBERS
# @dp.callback_query(F.data.startswith("mem_"))
# async def mem_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     await cb.message.edit_text("👥 <b>A'zolar</b>", parse_mode="HTML", reply_markup=get_member_menu(idx))
#     await cb.answer()

# @dp.callback_query(F.data.startswith("ban_"))
# async def ban_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_ban_user)
#     await cb.message.edit_text("🚫 <b>User ID:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_ban_user)
# async def ban_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         ban_uid = int(msg.text.strip())
#         await bot.ban_chat_member(chat_id=ch["id"], user_id=ban_uid)
#         write_log(uid, msg.from_user.username or "noname", "BANNED", f"User: {ban_uid}")
#         await msg.answer(f"✅ <b>Ban!</b>\n\n👤 {ban_uid}", parse_mode="HTML", reply_markup=get_main_menu())
#     except ValueError:
#         await msg.answer("❌ Faqat raqam!", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# @dp.callback_query(F.data.startswith("unb_"))
# async def unb_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_unban_user)
#     await cb.message.edit_text("✅ <b>User ID:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_unban_user)
# async def unb_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         unban_uid = int(msg.text.strip())
#         await bot.unban_chat_member(chat_id=ch["id"], user_id=unban_uid)
#         write_log(uid, msg.from_user.username or "noname", "UNBANNED", f"User: {unban_uid}")
#         await msg.answer(f"✅ <b>Unban!</b>\n\n👤 {unban_uid}", parse_mode="HTML", reply_markup=get_main_menu())
#     except ValueError:
#         await msg.answer("❌ Faqat raqam!", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# @dp.callback_query(F.data.startswith("res_"))
# async def res_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_restrict_user)
#     await cb.message.edit_text("⚠️ <b>User ID:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_restrict_user)
# async def res_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         res_uid = int(msg.text.strip())
#         perms = ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_polls=False)
#         await bot.restrict_chat_member(chat_id=ch["id"], user_id=res_uid, permissions=perms, until_date=datetime.now() + timedelta(days=365))
#         write_log(uid, msg.from_user.username or "noname", "RESTRICTED", f"User: {res_uid}")
#         await msg.answer(f"✅ <b>Restrict!</b>\n\n👤 {res_uid}", parse_mode="HTML", reply_markup=get_main_menu())
#     except ValueError:
#         await msg.answer("❌ Faqat raqam!", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# @dp.callback_query(F.data.startswith("pro_"))
# async def pro_cb(cb: CallbackQuery, state: FSMContext):
#     idx = int(cb.data.split("_")[1])
#     await state.update_data(idx=idx)
#     await state.set_state(ChannelStates.waiting_for_promote_user)
#     await cb.message.edit_text("⭐️ <b>User ID:</b>", parse_mode="HTML")
#     await cb.answer()

# @dp.message(ChannelStates.waiting_for_promote_user)
# async def pro_proc(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     idx = data.get("idx")
#     uid = msg.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await msg.answer("❌ Topilmadi!", reply_markup=get_main_menu())
#         await state.clear()
#         return
#     ch = user_channels[uid][idx]
#     try:
#         pro_uid = int(msg.text.strip())
#         await bot.promote_chat_member(chat_id=ch["id"], user_id=pro_uid, can_manage_chat=True, can_post_messages=True, can_edit_messages=True, can_delete_messages=True, can_restrict_members=True, can_promote_members=False, can_change_info=True, can_invite_users=True, can_pin_messages=True)
#         write_log(uid, msg.from_user.username or "noname", "PROMOTED", f"User: {pro_uid}")
#         await msg.answer(f"✅ <b>Admin!</b>\n\n👤 {pro_uid}", parse_mode="HTML", reply_markup=get_main_menu())
#     except ValueError:
#         await msg.answer("❌ Faqat raqam!", reply_markup=get_main_menu())
#     except Exception as e:
#         await msg.answer(f"❌ {str(e)[:100]}", reply_markup=get_main_menu())
#     await state.clear()

# # LINKS
# @dp.callback_query(F.data.startswith("link_"))
# async def link_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     await cb.message.edit_text("🔗 <b>Havolalar</b>", parse_mode="HTML", reply_markup=get_link_menu(idx))
#     await cb.answer()

# @dp.callback_query(F.data.startswith("explink_"))
# async def explink_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     uid = cb.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await cb.answer("❌ Topilmadi!", show_alert=True)
#         return
#     ch = user_channels[uid][idx]
#     try:
#         link = await bot.export_chat_invite_link(chat_id=ch["id"])
#         write_log(uid, cb.from_user.username or "noname", "LINK_EXPORTED", ch['name'])
#         await cb.message.edit_text(f"🔗 <b>Doimiy havola:</b>\n\n{link}", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="main")]]))
#     except Exception as e:
#         await cb.answer(f"❌ {str(e)[:50]}", show_alert=True)
#     await cb.answer()

# @dp.callback_query(F.data.startswith("crtlink_"))
# async def crtlink_cb(cb: CallbackQuery):
#     idx = int(cb.data.split("_")[1])
#     uid = cb.from_user.id
#     if uid not in user_channels or idx >= len(user_channels[uid]):
#         await cb.answer("❌ Topilmadi!", show_alert=True)
#         return
#     ch = user_channels[uid][idx]
#     try:
#         link = await bot.create_chat_invite_link(chat_id=ch["id"], expire_date=datetime.now() + timedelta(days=1), member_limit=100)
#         write_log(uid, cb.from_user.username or "noname", "LINK_CREATED", ch['name'])
#         await cb.message.edit_text(f"⏰ <b>Cheklangan:</b>\n\n{link.invite_link}\n\n⏰ 24h | 👥 100", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="main")]]))
#     except Exception as e:
#         await cb.answer(f"❌ {str(e)[:50]}", show_alert=True)
#     await cb.answer()

# # ADMIN
# @dp.message(Command("stats"))
# async def stats_cmd(msg: Message):
#     if msg.from_user.id != ADMIN_ID:
#         return
#     total_users = len(user_channels)
#     total_channels = sum(len(ch) for ch in user_channels.values())
#     await msg.answer(f"📊 <b>STATISTIKA</b>\n\n👥 Users: {total_users}\n📢 Channels: {total_channels}", parse_mode="HTML")

# @dp.message(Command("logs"))
# async def logs_cmd(msg: Message):
#     if msg.from_user.id != ADMIN_ID:
#         return
#     try:
#         if os.path.exists(LOG_FILE):
#             await msg.answer_document(FSInputFile(LOG_FILE), caption="📋 <b>Logs</b>", parse_mode="HTML")
#         else:
#             await msg.answer("❌ Yo'q")
#     except Exception as e:
#         await msg.answer(f"❌ {e}")

# @dp.message(Command("backup"))
# async def backup_cmd(msg: Message):
#     if msg.from_user.id != ADMIN_ID:
#         return
#     try:
#         if os.path.exists(DATA_FILE):
#             await msg.answer_document(FSInputFile(DATA_FILE), caption="💾 <b>Backup</b>", parse_mode="HTML")
#         else:
#             await msg.answer("❌ Yo'q")
#     except Exception as e:
#         await msg.answer(f"❌ {e}")

# @dp.message()
# async def unknown_msg(msg: Message):
#     await msg.answer("❓ /start", reply_markup=get_main_menu())

# # MAIN
# async def on_startup():
#     print("="*40)
#     print("🚀 BOT ISHGA TUSHDI!")
#     print(f"📊 Users: {len(user_channels)}")
#     print("="*40)
#     try:
#         await bot.send_message(ADMIN_ID, f"✅ <b>Bot ishga tushdi!</b>\n\n📊 {len(user_channels)} users", parse_mode="HTML")
#     except:
#         pass

# async def on_shutdown():
#     print("\n🛑 To'xtatildi!")
#     save_data(user_channels)
#     try:
#         await bot.send_message(ADMIN_ID, "🛑 <b>Bot to'xtatildi!</b>", parse_mode="HTML")
#     except:
#         pass

# async def main():
#     dp.startup.register(on_startup)
#     dp.shutdown.register(on_shutdown)
#     try:
#         await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
#     finally:
#         await bot.session.close()

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n⚠️ Ctrl+C")
#     except Exception as e:
#         print(f"\n❌ {e}")



import os
import asyncio
import json
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ChatPermissions, InputMediaPhoto, CallbackQuery, BufferedInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# .env fayldan o'qish
load_dotenv()

# CONFIG
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Tekshirish
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN .env faylda topilmadi!")
if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID .env faylda topilmadi!")

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    raise ValueError("❌ ADMIN_ID raqam bo'lishi kerak!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

DATA_FILE = "channels.json"
LOG_FILE = "logs.txt"

# DATABASE
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return {int(k): v for k, v in json.load(f).items()}
        return {}
    except:
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

user_channels = load_data()

# STATES
class ChannelStates(StatesGroup):
    waiting_for_channel_id = State()
    waiting_for_new_title = State()
    waiting_for_new_description = State()
    waiting_for_message = State()
    waiting_for_photo = State()
    waiting_for_media_group = State()
    waiting_for_poll = State()
    waiting_for_ban_user = State()
    waiting_for_unban_user = State()
    waiting_for_restrict_user = State()
    waiting_for_promote_user = State()
    waiting_for_pin_message = State()
    waiting_for_chat_photo = State()

# LOG
def write_log(user_id, username, action, details=""):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {user_id} (@{username}) | {action} | {details}\n")
        asyncio.create_task(bot.send_message(ADMIN_ID, f"📋 <b>{action}</b>\n👤 User: {user_id}\n📝 {details[:100]}", parse_mode="HTML"))
    except:
        pass

# KEYBOARDS
def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Kanal/Guruh Qo'shish", callback_data="add_channel")],
        [InlineKeyboardButton(text="📊 Mening Kanallarim", callback_data="my_channels")],
        [InlineKeyboardButton(text="❓ Yordam va Ko'rsatmalar", callback_data="help")]
    ])

def get_channel_list(user_id):
    kb = []
    if user_id in user_channels and user_channels[user_id]:
        for idx, ch in enumerate(user_channels[user_id]):
            emoji = "📢" if ch["type"] == "channel" else "👥"
            kb.append([InlineKeyboardButton(text=f"{emoji} {ch['name'][:30]}", callback_data=f"sel_{idx}")])
    kb.append([InlineKeyboardButton(text="🔙 Asosiy Menyuga", callback_data="main")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def get_channel_menu(idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 To'liq Ma'lumot", callback_data=f"info_{idx}"),
         InlineKeyboardButton(text="📤 Xabar Yuborish", callback_data=f"send_{idx}")],
        [InlineKeyboardButton(text="✏️ Nom O'zgartirish", callback_data=f"title_{idx}"),
         InlineKeyboardButton(text="📝 Tavsif O'zgartirish", callback_data=f"desc_{idx}")],
        [InlineKeyboardButton(text="🖼 Rasm Boshqaruvi", callback_data=f"pic_{idx}"),
         InlineKeyboardButton(text="📌 Pin Boshqaruvi", callback_data=f"pin_{idx}")],
        [InlineKeyboardButton(text="👥 A'zolar Boshqaruvi", callback_data=f"mem_{idx}"),
         InlineKeyboardButton(text="🔗 Taklif Havolasi", callback_data=f"link_{idx}")],
        [InlineKeyboardButton(text="🗑 Ro'yxatdan O'chirish", callback_data=f"del_{idx}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="my_channels")]
    ])

def get_send_menu(idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Oddiy Matn", callback_data=f"txt_{idx}"),
         InlineKeyboardButton(text="📸 Bitta Rasm", callback_data=f"pho_{idx}")],
        [InlineKeyboardButton(text="🖼 Bir Nechta Rasm", callback_data=f"med_{idx}"),
         InlineKeyboardButton(text="📊 So'rovnoma", callback_data=f"pol_{idx}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
    ])

def get_member_menu(idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚫 Ban (Bloklash)", callback_data=f"ban_{idx}"),
         InlineKeyboardButton(text="✅ Unban (Blokdan Chiqarish)", callback_data=f"unb_{idx}")],
        [InlineKeyboardButton(text="⚠️ Cheklash", callback_data=f"res_{idx}"),
         InlineKeyboardButton(text="⭐️ Admin Qilish", callback_data=f"pro_{idx}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
    ])

def get_pin_menu(idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 Xabarni Pinlash", callback_data=f"dopin_{idx}"),
         InlineKeyboardButton(text="📍 Pinni Olib Tashlash", callback_data=f"unpin_{idx}")],
        [InlineKeyboardButton(text="🚫 Barcha Pinlarni Olib Tashlash", callback_data=f"unpinall_{idx}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
    ])

def get_pic_menu(idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖼 Yangi Rasm O'rnatish", callback_data=f"setpic_{idx}"),
         InlineKeyboardButton(text="🗑 Rasmni O'chirish", callback_data=f"delpic_{idx}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
    ])

def get_link_menu(idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Doimiy Havola", callback_data=f"explink_{idx}"),
         InlineKeyboardButton(text="⏰ Vaqtinchalik Havola", callback_data=f"crtlink_{idx}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
    ])

# START
@dp.message(Command("start"))
async def start_cmd(msg: Message):
    write_log(msg.from_user.id, msg.from_user.username or "noname", "BOT_ISHGA_TUSHDI", "")
    welcome_text = """
🤖 <b>Telegram Kanal Boshqaruv Botiga Xush Kelibsiz!</b>

Bu bot orqali siz:
✅ Kanallaringizni va guruhlaringizni boshqarishingiz
✅ Xabarlar yuborishingiz
✅ A'zolarni boshqarishingiz
✅ Va boshqa ko'plab imkoniyatlardan foydalanishingiz mumkin!

<b>⚠️ Muhim:</b> Botni ishlashi uchun uni kanal/guruhingizda <b>ADMIN</b> qilishingiz shart!

📌 Quyidagi tugmalardan foydalaning:
"""
    await msg.answer(welcome_text, parse_mode="HTML", reply_markup=get_main_menu())

@dp.callback_query(F.data == "main")
async def main_cb(cb: CallbackQuery):
    await cb.message.edit_text(
        "🏠 <b>Asosiy Menyu</b>\n\nKerakli bo'limni tanlang:", 
        parse_mode="HTML", 
        reply_markup=get_main_menu()
    )
    await cb.answer()

@dp.callback_query(F.data == "help")
async def help_cb(cb: CallbackQuery):
    help_text = """
❓ <b>YORDAM VA KO'RSATMALAR</b>

<b>1️⃣ Kanal/Guruh Qo'shish:</b>
   • "➕ Kanal Qo'shish" tugmasini bosing
   • Botni kanal/guruhingizda <u>ADMIN</u> qilib qo'ying
   • Kanal ID yoki @username ni yuboring
   • Misol: <code>-1001234567890</code> yoki <code>@kanalim</code>

<b>2️⃣ Kanal ID Topish:</b>
   • Kanalga kiring
   • Biror xabarni Forward qiling @userinfobot ga
   • U sizga kanal ID ni beradi

<b>3️⃣ Admin Huquqlari:</b>
   Bot quyidagi huquqlarga ega bo'lishi kerak:
   ✓ Xabar yuborish
   ✓ Xabarlarni o'chirish
   ✓ A'zolarni boshqarish
   ✓ Kanal ma'lumotlarini o'zgartirish

<b>👨‍💼 Admin Komandalar:</b>
/stats - Statistika
/logs - Faoliyat jurnali
/backup - Zaxira nusxa

<b>🆘 Muammo bo'lsa:</b>
Botning admin huquqlarini tekshiring!
admin: @bynoutbook
"""
    await cb.message.edit_text(
        help_text, 
        parse_mode="HTML", 
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Asosiy Menyuga", callback_data="main")]
        ])
    )
    await cb.answer()

# ADD CHANNEL
@dp.callback_query(F.data == "add_channel")
async def add_ch_cb(cb: CallbackQuery, state: FSMContext):
    instruction_text = """
📝 <b>Kanal yoki Guruh Qo'shish</b>

<b>⚠️ MUHIM - Avval Botni Admin Qiling!</b>

<b>Qadamlar:</b>
1️⃣ Kanal/guruhingizga kiring
2️⃣ "Administrators" bo'limiga o'ting
3️⃣ "Add Admin" tugmasini bosing
4️⃣ @chanadbot ni toping va admin qiling
5️⃣ Barcha kerakli huquqlarni bering

<b>Keyin bu yerga quyidagilardan birini yuboring:</b>

📌 <b>Kanal ID:</b> <code>-1001234567890</code>
📌 <b>Kanal Username:</b> <code>@mening_kanalim</code>

<b>💡 Maslahat:</b> 
Kanal ID ni topish uchun @userinfobot dan foydalaning!
Kanal xabarini unga forward qiling.
"""
    await cb.message.edit_text(instruction_text, parse_mode="HTML")
    await state.set_state(ChannelStates.waiting_for_channel_id)
    await cb.answer()

@dp.message(ChannelStates.waiting_for_channel_id)
async def add_ch_proc(msg: Message, state: FSMContext):
    ch_id = msg.text.strip()
    processing_msg = await msg.answer("⏳ <b>Tekshirilmoqda...</b>", parse_mode="HTML")
    
    try:
        # Kanal ma'lumotlarini olish
        chat = await bot.get_chat(chat_id=ch_id)
        
        # Bot statusini tekshirish
        bot_mem = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
        
        if bot_mem.status not in ["administrator", "creator"]:
            error_text = f"""
❌ <b>XATOLIK: Bot Admin Emas!</b>

📢 <b>Kanal:</b> {chat.title}
🆔 <b>ID:</b> <code>{chat.id}</code>

<b>⚠️ Muammo:</b> Bot bu kanal/guruhda admin huquqlariga ega emas.

<b>✅ Yechim:</b>
1. Kanal/guruhga kiring
2. Botni admin qilib qo'ying
3. Qaytadan urinib ko'ring

<b>🔧 Kerakli huquqlar:</b>
• Xabar yuborish
• Xabarlarni o'zgartirish va o'chirish
• Foydalanuvchilarni boshqarish
• Kanal ma'lumotlarini o'zgartirish
"""
            await processing_msg.edit_text(error_text, parse_mode="HTML", reply_markup=get_main_menu())
            await state.clear()
            return
        
        uid = msg.from_user.id
        if uid not in user_channels:
            user_channels[uid] = []
        
        # Takrorlanish tekshiruvi
        if any(c["id"] == chat.id for c in user_channels[uid]):
            await processing_msg.edit_text(
                f"⚠️ <b>Bu kanal allaqachon ro'yxatda!</b>\n\n📢 {chat.title}", 
                parse_mode="HTML", 
                reply_markup=get_main_menu()
            )
            await state.clear()
            return
        
        # Kanalni qo'shish
        user_channels[uid].append({
            "id": chat.id, 
            "username": chat.username or "yo'q", 
            "name": chat.title, 
            "type": chat.type, 
            "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_data(user_channels)
        write_log(uid, msg.from_user.username or "noname", "KANAL_QO'SHILDI", f"{chat.title} ({chat.id})")
        
        success_text = f"""
✅ <b>Muvaffaqiyatli Qo'shildi!</b>

📢 <b>Nom:</b> {chat.title}
🆔 <b>ID:</b> <code>{chat.id}</code>
🔗 <b>Username:</b> @{chat.username or 'yo\'q'}
📅 <b>Qo'shilgan:</b> {datetime.now().strftime("%d.%m.%Y %H:%M")}

Endi siz bu kanalni to'liq boshqarishingiz mumkin! 🎉
"""
        await processing_msg.edit_text(success_text, parse_mode="HTML", reply_markup=get_main_menu())
        
    except Exception as e:
        error_detail = str(e)
        if "chat not found" in error_detail.lower():
            error_msg = """
❌ <b>Kanal Topilmadi!</b>

<b>Mumkin bo'lgan sabablar:</b>
• Noto'g'ri ID yoki username
• Kanal privat va bot a'zo emas
• ID xato yozilgan

<b>✅ To'g'ri formatlar:</b>
<code>-1001234567890</code> (ID)
<code>@kanalim</code> (Username)
"""
        elif "forbidden" in error_detail.lower():
            error_msg = """
❌ <b>Kirish Taqiqlangan!</b>

Bot bu kanalga kirish huquqiga ega emas.

<b>Yechim:</b>
1. Botni kanalga qo'shing
2. Admin qiling
3. Qaytadan urinib ko'ring
"""
        else:
            error_msg = f"❌ <b>Xatolik:</b>\n\n<code>{error_detail[:200]}</code>\n\n💡 Qaytadan urinib ko'ring yoki admin bilan bog'laning."
        
        await processing_msg.edit_text(error_msg, parse_mode="HTML", reply_markup=get_main_menu())
    
    await state.clear()

# QISM 2/3 - Bu faylni birinchi qismdan keyin qo'shing

# MY CHANNELS
@dp.callback_query(F.data == "my_channels")
async def my_ch_cb(cb: CallbackQuery):
    uid = cb.from_user.id
    if uid not in user_channels or not user_channels[uid]:
        await cb.message.edit_text(
            "📭 <b>Sizda hali kanal yo'q!</b>\n\nBirinchi kanalingizni qo'shish uchun quyidagi tugmani bosing:", 
            parse_mode="HTML", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="➕ Kanal Qo'shish", callback_data="add_channel")],
                [InlineKeyboardButton(text="🔙 Asosiy Menyuga", callback_data="main")]
            ])
        )
    else:
        await cb.message.edit_text(
            f"📊 <b>Sizning Kanallaringiz</b>\n\nJami: <b>{len(user_channels[uid])} ta</b>\n\nBoshqarish uchun tanlang:", 
            parse_mode="HTML", 
            reply_markup=get_channel_list(uid)
        )
    await cb.answer()

@dp.callback_query(F.data.startswith("sel_"))
async def sel_ch_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    ch = user_channels[uid][idx]
    emoji = "📢" if ch["type"] == "channel" else "👥"
    detail_text = f"""
{emoji} <b>{ch['name']}</b>

🆔 <b>ID:</b> <code>{ch['id']}</code>
📅 <b>Qo'shilgan:</b> {ch['added']}
🔗 <b>Username:</b> @{ch.get('username', 'yo\'q')}

<b>Boshqaruv menyusidan tanlang:</b>
"""
    await cb.message.edit_text(detail_text, parse_mode="HTML", reply_markup=get_channel_menu(idx))
    await cb.answer()

@dp.callback_query(F.data.startswith("del_"))
async def del_ch_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    ch = user_channels[uid].pop(idx)
    save_data(user_channels)
    write_log(uid, cb.from_user.username or "noname", "KANAL_O'CHIRILDI", ch['name'])
    await cb.message.edit_text(
        f"✅ <b>Ro'yxatdan O'chirildi!</b>\n\n📢 <b>{ch['name']}</b>\n\n⚠️ Kanal o'zi o'chirilmadi, faqat botdan olib tashlandi.", 
        parse_mode="HTML", 
        reply_markup=get_main_menu()
    )
    await cb.answer()

@dp.callback_query(F.data.startswith("info_"))
async def info_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    ch = user_channels[uid][idx]
    try:
        chat = await bot.get_chat(chat_id=ch["id"])
        count = await bot.get_chat_member_count(chat_id=ch["id"])
        
        info_text = f"""
📊 <b>TO'LIQ MA'LUMOT</b>

📢 <b>Nom:</b> {chat.title}
🆔 <b>ID:</b> <code>{chat.id}</code>
🔗 <b>Username:</b> @{chat.username or 'Yo\'q'}
👥 <b>A\'zolar:</b> {count:,} ta
📖 <b>Tavsif:</b> {chat.description or 'Tavsif kiritilmagan'}
🔒 <b>Tur:</b> {'📢 Kanal' if chat.type == 'channel' else '👥 Guruh'}
📅 <b>Qo\'shilgan:</b> {ch['added']}
"""
        await cb.message.edit_text(
            info_text, 
            parse_mode="HTML", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"sel_{idx}")]
            ])
        )
    except Exception as e:
        await cb.answer(f"❌ Ma'lumot olishda xatolik: {str(e)[:50]}", show_alert=True)
    await cb.answer()

# TITLE
@dp.callback_query(F.data.startswith("title_"))
async def title_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_new_title)
    await cb.message.edit_text(
        "✏️ <b>Kanal Nomini O'zgartirish</b>\n\nYangi nomni yuboring:\n\n💡 <i>Nom 1-128 belgi orasida bo'lishi kerak</i>", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_new_title)
async def title_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    new_title = msg.text.strip()
    if len(new_title) < 1 or len(new_title) > 128:
        await msg.answer("❌ Nom 1-128 belgi orasida bo'lishi kerak!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    ch = user_channels[uid][idx]
    
    try:
        await bot.set_chat_title(chat_id=ch["id"], title=new_title)
        old_name = user_channels[uid][idx]["name"]
        user_channels[uid][idx]["name"] = new_title
        save_data(user_channels)
        write_log(uid, msg.from_user.username or "noname", "NOM_O'ZGARTIRILDI", f"{old_name} → {new_title}")
        
        await msg.answer(
            f"✅ <b>Nom O'zgartirildi!</b>\n\n📝 <b>Eski:</b> {old_name}\n📝 <b>Yangi:</b> {new_title}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        error_text = f"❌ <b>Xatolik yuz berdi!</b>\n\n{str(e)[:150]}\n\n💡 Bot admin huquqlariga ega ekanligini tekshiring!"
        await msg.answer(error_text, parse_mode="HTML", reply_markup=get_main_menu())
    await state.clear()

# DESCRIPTION
@dp.callback_query(F.data.startswith("desc_"))
async def desc_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_new_description)
    await cb.message.edit_text(
        "📝 <b>Kanal Tavsifini O'zgartirish</b>\n\nYangi tavsifni yuboring:\n\n💡 <i>Tavsif 0-255 belgi orasida bo'lishi kerak</i>", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_new_description)
async def desc_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    new_desc = msg.text.strip()
    if len(new_desc) > 255:
        await msg.answer("❌ Tavsif 255 belgidan oshmasligi kerak!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    ch = user_channels[uid][idx]
    
    try:
        await bot.set_chat_description(chat_id=ch["id"], description=new_desc)
        write_log(uid, msg.from_user.username or "noname", "TAVSIF_O'ZGARTIRILDI", f"{ch['name']}: {new_desc[:50]}")
        await msg.answer(
            f"✅ <b>Tavsif O'zgartirildi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n📝 <b>Yangi tavsif:</b> {new_desc[:100]}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        await msg.answer(
            f"❌ <b>Xatolik!</b>\n\n{str(e)[:150]}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    await state.clear()

# SEND MENU
@dp.callback_query(F.data.startswith("send_"))
async def send_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    await cb.message.edit_text(
        "📤 <b>Xabar Yuborish Turi</b>\n\nQanday turdagi xabar yubormoqchisiz?", 
        parse_mode="HTML", 
        reply_markup=get_send_menu(idx)
    )
    await cb.answer()

@dp.callback_query(F.data.startswith("txt_"))
async def txt_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_message)
    await cb.message.edit_text(
        "💬 <b>Matnli Xabar Yuborish</b>\n\nXabar matnini yuboring:\n\n💡 HTML formatdan foydalanishingiz mumkin:\n• <code>&lt;b&gt;Qalin&lt;/b&gt;</code>\n• <code>&lt;i&gt;Kursiv&lt;/i&gt;</code>\n• <code>&lt;code&gt;Kod&lt;/code&gt;</code>", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_message)
async def txt_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    ch = user_channels[uid][idx]
    try:
        sent_msg = await bot.send_message(chat_id=ch["id"], text=msg.text, parse_mode="HTML")
        write_log(uid, msg.from_user.username or "noname", "MATN_YUBORILDI", f"{ch['name']}: {msg.text[:50]}")
        await msg.answer(
            f"✅ <b>Xabar Yuborildi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n🆔 <b>Xabar ID:</b> {sent_msg.message_id}\n📝 {msg.text[:100]}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        await msg.answer(f"❌ <b>Yuborishda xatolik!</b>\n\n{str(e)[:200]}", parse_mode="HTML", reply_markup=get_main_menu())
    await state.clear()

@dp.callback_query(F.data.startswith("pho_"))
async def pho_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_photo)
    await cb.message.edit_text(
        "📸 <b>Rasm Yuborish</b>\n\nRasm yuboring:\n\n💡 Rasm bilan birga caption (izoh) ham yozishingiz mumkin", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_photo, F.photo)
async def pho_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    ch = user_channels[uid][idx]
    try:
        sent_msg = await bot.send_photo(
            chat_id=ch["id"], 
            photo=msg.photo[-1].file_id, 
            caption=msg.caption, 
            parse_mode="HTML"
        )
        write_log(uid, msg.from_user.username or "noname", "RASM_YUBORILDI", f"{ch['name']}")
        await msg.answer(
            f"✅ <b>Rasm Yuborildi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n🆔 <b>Xabar ID:</b> {sent_msg.message_id}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        await msg.answer(f"❌ <b>Xatolik!</b>\n\n{str(e)[:150]}", parse_mode="HTML", reply_markup=get_main_menu())
    await state.clear()

@dp.callback_query(F.data.startswith("med_"))
async def med_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx, media=[])
    await state.set_state(ChannelStates.waiting_for_media_group)
    await cb.message.edit_text(
        "🖼 <b>Bir Nechta Rasm Yuborish</b>\n\nRasmlarni ketma-ket yuboring (2-10 ta)\n\n✅ Rasmlar to'plangach /done yozing\n❌ Bekor qilish: /cancel", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_media_group, F.photo)
async def med_collect(msg: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    
    if len(media) >= 10:
        await msg.answer("⚠️ Maksimal 10 ta rasm! /done yozing")
        return
    
    media.append({"file_id": msg.photo[-1].file_id, "caption": msg.caption})
    await state.update_data(media=media)
    await msg.answer(
        f"✅ <b>{len(media)} ta rasm qo'shildi</b>\n\n➕ Yana yuboring yoki /done yozing", 
        parse_mode="HTML"
    )

@dp.message(ChannelStates.waiting_for_media_group, Command("done"))
async def med_done(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    media = data.get("media", [])
    uid = msg.from_user.id
    
    if not media or len(media) < 2:
        await msg.answer("❌ Kamida 2 ta rasm kerak!\n\nYana rasm yuboring yoki /cancel", reply_markup=get_main_menu())
        return
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    ch = user_channels[uid][idx]
    processing = await msg.answer("⏳ Yuborilmoqda...")
    
    try:
        group = []
        for i, m in enumerate(media):
            if i == 0 and m.get("caption"):
                group.append(InputMediaPhoto(media=m["file_id"], caption=m["caption"], parse_mode="HTML"))
            else:
                group.append(InputMediaPhoto(media=m["file_id"]))
        
        await bot.send_media_group(chat_id=ch["id"], media=group)
        write_log(uid, msg.from_user.username or "noname", "MEDIA_YUBORILDI", f"{ch['name']}: {len(media)} ta rasm")
        
        await processing.edit_text(
            f"✅ <b>Rasmlar Yuborildi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n🖼 <b>Soni:</b> {len(media)} ta", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        await processing.edit_text(f"❌ <b>Xatolik!</b>\n\n{str(e)[:150]}", parse_mode="HTML", reply_markup=get_main_menu())
    
    await state.clear()

@dp.message(ChannelStates.waiting_for_media_group, Command("cancel"))
async def med_cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("❌ Bekor qilindi", reply_markup=get_main_menu())

@dp.callback_query(F.data.startswith("pol_"))
async def pol_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_poll)
    await cb.message.edit_text(
        "📊 <b>So'rovnoma Yuborish</b>\n\n<b>Format:</b>\nSavol\nVariant 1\nVariant 2\nVariant 3\n...\n\n<b>Misol:</b>\nEnglizmi yoqtirasz?\nHa\nYo'q\nBilmayman\n\n💡 Har bir qatorga 1 ta variant", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_poll)
async def pol_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    lines = [l.strip() for l in msg.text.strip().split("\n") if l.strip()]
    
    if len(lines) < 3:
        await msg.answer("❌ Kamida 1 savol va 2 variant kerak!", reply_markup=get_main_menu())
        return
    
    if len(lines) > 11:
        await msg.answer("❌ Maksimal 10 variant bo'lishi mumkin!", reply_markup=get_main_menu())
        return
    
    question = lines[0]
    options = lines[1:]
    ch = user_channels[uid][idx]
    
    try:
        sent_poll = await bot.send_poll(
            chat_id=ch["id"], 
            question=question, 
            options=options, 
            is_anonymous=True
        )
        write_log(uid, msg.from_user.username or "noname", "SO'ROVNOMA_YUBORILDI", f"{ch['name']}: {question[:30]}")
        await msg.answer(
            f"✅ <b>So'rovnoma Yuborildi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n❓ <b>Savol:</b> {question}\n📊 <b>Variantlar:</b> {len(options)} ta", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        await msg.answer(f"❌ <b>Xatolik!</b>\n\n{str(e)[:150]}", parse_mode="HTML", reply_markup=get_main_menu())
    
    await state.clear()

# PICTURE - TO'G'RILANGAN
@dp.callback_query(F.data.startswith("pic_"))
async def pic_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    await cb.message.edit_text(
        "🖼 <b>Kanal Rasmini Boshqarish</b>\n\nQuyidagilardan birini tanlang:", 
        parse_mode="HTML", 
        reply_markup=get_pic_menu(idx)
    )
    await cb.answer()

@dp.callback_query(F.data.startswith("setpic_"))
async def setpic_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_chat_photo)
    await cb.message.edit_text(
        "🖼 <b>Kanal Rasmini O'rnatish</b>\n\nYangi rasmni yuboring:\n\n💡 Rasm yuqori sifatli va kvadrat shaklda bo'lishi tavsiya etiladi", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_chat_photo, F.photo)
async def setpic_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    ch = user_channels[uid][idx]
    processing = await msg.answer("⏳ O'rnatilmoqda...")
    
    try:
        # Rasmni yuklash
        file = await bot.get_file(msg.photo[-1].file_id)
        photo_bytes = await bot.download_file(file.file_path)
        
        # BufferedInputFile dan foydalanish - fayl tizimiga saqlamasdan
        input_file = BufferedInputFile(photo_bytes.read(), filename="photo.jpg")
        
        # Kanal rasmini o'rnatish
        await bot.set_chat_photo(chat_id=ch["id"], photo=input_file)
        
        write_log(uid, msg.from_user.username or "noname", "RASM_O'RNATILDI", f"{ch['name']}")
        
        await processing.edit_text(
            f"✅ <b>Rasm Muvaffaqiyatli O'rnatildi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n🖼 Yangi rasm faol", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        error_msg = str(e)
        if "not enough rights" in error_msg.lower():
            await processing.edit_text(
                "❌ <b>Huquq yetishmayapti!</b>\n\nBot kanalda rasm o'zgartirish huquqiga ega emas.\n\n<b>Yechim:</b> Bot adminlik huquqlarini tekshiring", 
                parse_mode="HTML", 
                reply_markup=get_main_menu()
            )
        else:
            await processing.edit_text(
                f"❌ <b>Xatolik!</b>\n\n{error_msg[:200]}", 
                parse_mode="HTML", 
                reply_markup=get_main_menu()
            )
    
    await state.clear()

@dp.callback_query(F.data.startswith("delpic_"))
async def delpic_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    ch = user_channels[uid][idx]
    try:
        await bot.delete_chat_photo(chat_id=ch["id"])
        write_log(uid, cb.from_user.username or "noname", "RASM_O'CHIRILDI", ch['name'])
        await cb.message.edit_text(
            f"✅ <b>Rasm O'chirildi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        error_msg = str(e)
        if "photo not found" in error_msg.lower():
            await cb.answer("⚠️ Kanalda rasm mavjud emas!", show_alert=True)
        else:
            await cb.answer(f"❌ {error_msg[:80]}", show_alert=True)
    await cb.answer()

# QISM 3/3 - Bu faylni ikkinchi qismdan keyin qo'shing

# PIN
@dp.callback_query(F.data.startswith("pin_"))
async def pin_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    await cb.message.edit_text(
        "📌 <b>Xabarni Pin Qilish</b>\n\nQuyidagi amallardan birini tanlang:", 
        parse_mode="HTML", 
        reply_markup=get_pin_menu(idx)
    )
    await cb.answer()

@dp.callback_query(F.data.startswith("dopin_"))
async def dopin_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_pin_message)
    await cb.message.edit_text(
        "📌 <b>Xabarni Pin Qilish</b>\n\nPin qilmoqchi bo'lgan xabar ID sini yuboring:\n\n💡 <b>Xabar ID ni qanday topish kerak?</b>\n1. Kanalga kiring\n2. Xabarni bosib turing\n3. 'Copy Message Link' tanlang\n4. Havoladagi oxirgi raqam - bu ID\n\n<b>Misol:</b> <code>12345</code>", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_pin_message)
async def dopin_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    ch = user_channels[uid][idx]
    
    try:
        msg_id = int(msg.text.strip())
        await bot.pin_chat_message(chat_id=ch["id"], message_id=msg_id, disable_notification=False)
        write_log(uid, msg.from_user.username or "noname", "XABAR_PINLANDI", f"{ch['name']}: ID {msg_id}")
        await msg.answer(
            f"✅ <b>Xabar Pin Qilindi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n🆔 <b>Xabar ID:</b> {msg_id}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except ValueError:
        await msg.answer("❌ <b>Xato format!</b>\n\nFaqat raqam kiriting, masalan: <code>12345</code>", parse_mode="HTML", reply_markup=get_main_menu())
    except Exception as e:
        error_msg = str(e)
        if "message not found" in error_msg.lower():
            await msg.answer("❌ <b>Xabar topilmadi!</b>\n\nID ni to'g'ri yozganingizga ishonch hosil qiling", parse_mode="HTML", reply_markup=get_main_menu())
        else:
            await msg.answer(f"❌ <b>Xatolik!</b>\n\n{error_msg[:150]}", parse_mode="HTML", reply_markup=get_main_menu())
    
    await state.clear()

@dp.callback_query(F.data.startswith("unpin_"))
async def unpin_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    
    ch = user_channels[uid][idx]
    try:
        await bot.unpin_chat_message(chat_id=ch["id"])
        write_log(uid, cb.from_user.username or "noname", "PIN_OLIB_TASHLANDI", ch['name'])
        await cb.message.edit_text(
            f"✅ <b>Oxirgi Pin Olib Tashlandi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        error_msg = str(e)
        if "no pinned message" in error_msg.lower():
            await cb.answer("⚠️ Kanalda pin qilingan xabar yo'q!", show_alert=True)
        else:
            await cb.answer(f"❌ {error_msg[:80]}", show_alert=True)
    
    await cb.answer()

@dp.callback_query(F.data.startswith("unpinall_"))
async def unpinall_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    
    ch = user_channels[uid][idx]
    try:
        await bot.unpin_all_chat_messages(chat_id=ch["id"])
        write_log(uid, cb.from_user.username or "noname", "BARCHA_PINLAR_OLIB_TASHLANDI", ch['name'])
        await cb.message.edit_text(
            f"✅ <b>Barcha Pinlar Olib Tashlandi!</b>\n\n📢 <b>Kanal:</b> {ch['name']}", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except Exception as e:
        await cb.answer(f"❌ Xatolik: {str(e)[:60]}", show_alert=True)
    
    await cb.answer()

# MEMBERS
@dp.callback_query(F.data.startswith("mem_"))
async def mem_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    
    ch = user_channels[uid][idx]
    
    # Guruh yoki kanal ekanligini tekshirish
    if ch["type"] == "channel":
        await cb.answer("⚠️ Bu funksiya faqat guruhlar uchun!", show_alert=True)
        return
    
    await cb.message.edit_text(
        f"👥 <b>A'zolarni Boshqarish</b>\n\n📢 <b>Guruh:</b> {ch['name']}\n\nQuyidagi amallardan birini tanlang:", 
        parse_mode="HTML", 
        reply_markup=get_member_menu(idx)
    )
    await cb.answer()

@dp.callback_query(F.data.startswith("ban_"))
async def ban_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_ban_user)
    await cb.message.edit_text(
        "🚫 <b>Foydalanuvchini Bloklash (Ban)</b>\n\nBloklash uchun user ID ni yuboring:\n\n💡 <b>User ID ni qanday topish kerak?</b>\n• Foydalanuvchini @userinfobot ga forward qiling\n• Yoki shunchaki user ID raqamini yozing\n\n<b>Misol:</b> <code>123456789</code>", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_ban_user)
async def ban_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    ch = user_channels[uid][idx]
    
    try:
        ban_uid = int(msg.text.strip())
        await bot.ban_chat_member(chat_id=ch["id"], user_id=ban_uid)
        write_log(uid, msg.from_user.username or "noname", "FOYDALANUVCHI_BLOKLANDI", f"{ch['name']}: User {ban_uid}")
        await msg.answer(
            f"✅ <b>Foydalanuvchi Bloklandi!</b>\n\n👥 <b>Guruh:</b> {ch['name']}\n👤 <b>User ID:</b> <code>{ban_uid}</code>\n\n⚠️ Bu foydalanuvchi guruhga qayta kira olmaydi", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except ValueError:
        await msg.answer("❌ <b>Xato format!</b>\n\nFaqat raqam kiriting: <code>123456789</code>", parse_mode="HTML", reply_markup=get_main_menu())
    except Exception as e:
        await msg.answer(f"❌ <b>Xatolik!</b>\n\n{str(e)[:200]}", parse_mode="HTML", reply_markup=get_main_menu())
    
    await state.clear()

@dp.callback_query(F.data.startswith("unb_"))
async def unb_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_unban_user)
    await cb.message.edit_text(
        "✅ <b>Foydalanuvchini Blokdan Chiqarish</b>\n\nBlokdan chiqarish uchun user ID ni yuboring:\n\n<b>Misol:</b> <code>123456789</code>", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_unban_user)
async def unb_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    ch = user_channels[uid][idx]
    
    try:
        unban_uid = int(msg.text.strip())
        await bot.unban_chat_member(chat_id=ch["id"], user_id=unban_uid)
        write_log(uid, msg.from_user.username or "noname", "FOYDALANUVCHI_BLOKDAN_CHIQARILDI", f"{ch['name']}: User {unban_uid}")
        await msg.answer(
            f"✅ <b>Blokdan Chiqarildi!</b>\n\n👥 <b>Guruh:</b> {ch['name']}\n👤 <b>User ID:</b> <code>{unban_uid}</code>\n\n✅ Endi guruhga qayta kirishi mumkin", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except ValueError:
        await msg.answer("❌ Faqat raqam kiriting!", reply_markup=get_main_menu())
    except Exception as e:
        await msg.answer(f"❌ {str(e)[:150]}", reply_markup=get_main_menu())
    
    await state.clear()

@dp.callback_query(F.data.startswith("res_"))
async def res_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_restrict_user)
    await cb.message.edit_text(
        "⚠️ <b>Foydalanuvchini Cheklash</b>\n\nCheklash uchun user ID ni yuboring:\n\n💡 <b>Cheklovlar:</b>\n• Xabar yoza olmaydi\n• Media yubora olmaydi\n• So'rovnoma yarata olmaydi\n• 1 yil davomida\n\n<b>Misol:</b> <code>123456789</code>", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_restrict_user)
async def res_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    ch = user_channels[uid][idx]
    
    try:
        res_uid = int(msg.text.strip())
        perms = ChatPermissions(
            can_send_messages=False, 
            can_send_media_messages=False, 
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )
        await bot.restrict_chat_member(
            chat_id=ch["id"], 
            user_id=res_uid, 
            permissions=perms, 
            until_date=datetime.now() + timedelta(days=365)
        )
        write_log(uid, msg.from_user.username or "noname", "FOYDALANUVCHI_CHEKLANDI", f"{ch['name']}: User {res_uid}")
        await msg.answer(
            f"✅ <b>Foydalanuvchi Cheklandi!</b>\n\n👥 <b>Guruh:</b> {ch['name']}\n👤 <b>User ID:</b> <code>{res_uid}</code>\n⏰ <b>Muddat:</b> 1 yil\n\n⚠️ Guruhda qoladi, lekin yoza olmaydi", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except ValueError:
        await msg.answer("❌ Faqat raqam kiriting!", reply_markup=get_main_menu())
    except Exception as e:
        await msg.answer(f"❌ {str(e)[:150]}", reply_markup=get_main_menu())
    
    await state.clear()

@dp.callback_query(F.data.startswith("pro_"))
async def pro_cb(cb: CallbackQuery, state: FSMContext):
    idx = int(cb.data.split("_")[1])
    await state.update_data(idx=idx)
    await state.set_state(ChannelStates.waiting_for_promote_user)
    await cb.message.edit_text(
        "⭐️ <b>Foydalanuvchini Admin Qilish</b>\n\nAdmin qilish uchun user ID ni yuboring:\n\n💡 <b>Admin huquqlari:</b>\n• Guruhni boshqarish\n• Xabar yuborish va o'chirish\n• A'zolarni boshqarish\n• Guruh ma'lumotlarini o'zgartirish\n• A'zo qo'shish va pin qilish\n\n⚠️ Boshqa adminlar qo'sha olmaydi\n\n<b>Misol:</b> <code>123456789</code>", 
        parse_mode="HTML"
    )
    await cb.answer()

@dp.message(ChannelStates.waiting_for_promote_user)
async def pro_proc(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("idx")
    uid = msg.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await msg.answer("❌ Kanal topilmadi!", reply_markup=get_main_menu())
        await state.clear()
        return
    
    ch = user_channels[uid][idx]
    
    try:
        pro_uid = int(msg.text.strip())
        await bot.promote_chat_member(
            chat_id=ch["id"], 
            user_id=pro_uid, 
            can_manage_chat=True, 
            can_post_messages=True, 
            can_edit_messages=True, 
            can_delete_messages=True, 
            can_restrict_members=True, 
            can_promote_members=False,
            can_change_info=True, 
            can_invite_users=True, 
            can_pin_messages=True
        )
        write_log(uid, msg.from_user.username or "noname", "ADMIN_QILINDI", f"{ch['name']}: User {pro_uid}")
        await msg.answer(
            f"✅ <b>Admin Qilindi!</b>\n\n👥 <b>Guruh:</b> {ch['name']}\n👤 <b>User ID:</b> <code>{pro_uid}</code>\n⭐️ <b>Status:</b> Administrator\n\n🎉 Endi bu foydalanuvchi guruhni boshqarishi mumkin!", 
            parse_mode="HTML", 
            reply_markup=get_main_menu()
        )
    except ValueError:
        await msg.answer("❌ Faqat raqam kiriting!", reply_markup=get_main_menu())
    except Exception as e:
        error_msg = str(e)
        if "user not found" in error_msg.lower():
            await msg.answer("❌ <b>Foydalanuvchi topilmadi!</b>\n\nU guruhda ekanligiga ishonch hosil qiling", parse_mode="HTML", reply_markup=get_main_menu())
        else:
            await msg.answer(f"❌ {error_msg[:200]}", reply_markup=get_main_menu())
    
    await state.clear()

# LINKS
@dp.callback_query(F.data.startswith("link_"))
async def link_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    await cb.message.edit_text(
        "🔗 <b>Taklif Havolasi Yaratish</b>\n\nQuyidagi turlardan birini tanlang:", 
        parse_mode="HTML", 
        reply_markup=get_link_menu(idx)
    )
    await cb.answer()

@dp.callback_query(F.data.startswith("explink_"))
async def explink_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    
    ch = user_channels[uid][idx]
    processing = await cb.message.edit_text("⏳ Havola yaratilmoqda...")
    
    try:
        link = await bot.export_chat_invite_link(chat_id=ch["id"])
        write_log(uid, cb.from_user.username or "noname", "DOIMIY_HAVOLA_YARATILDI", f"{ch['name']}")
        await processing.edit_text(
            f"🔗 <b>Doimiy Taklif Havolasi</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n\n<code>{link}</code>\n\n✅ Bu havola doim ishlaydi\n♾️ Cheksiz foydalanish\n\n💡 Havolani nusxalash uchun ustiga bosing", 
            parse_mode="HTML", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Asosiy Menyuga", callback_data="main")]
            ])
        )
    except Exception as e:
        await processing.edit_text(f"❌ Xatolik: {str(e)[:100]}", reply_markup=get_main_menu())
    
    await cb.answer()

@dp.callback_query(F.data.startswith("crtlink_"))
async def crtlink_cb(cb: CallbackQuery):
    idx = int(cb.data.split("_")[1])
    uid = cb.from_user.id
    
    if uid not in user_channels or idx >= len(user_channels[uid]):
        await cb.answer("❌ Kanal topilmadi!", show_alert=True)
        return
    
    ch = user_channels[uid][idx]
    processing = await cb.message.edit_text("⏳ Havola yaratilmoqda...")
    
    try:
        link = await bot.create_chat_invite_link(
            chat_id=ch["id"], 
            expire_date=datetime.now() + timedelta(hours=24), 
            member_limit=100
        )
        write_log(uid, cb.from_user.username or "noname", "VAQTINCHALIK_HAVOLA_YARATILDI", f"{ch['name']}")
        await processing.edit_text(
            f"⏰ <b>Vaqtinchalik Taklif Havolasi</b>\n\n📢 <b>Kanal:</b> {ch['name']}\n\n<code>{link.invite_link}</code>\n\n⏰ <b>Amal qilish:</b> 24 soat\n👥 <b>Max a'zolar:</b> 100 ta\n📅 <b>Muddati:</b> {(datetime.now() + timedelta(hours=24)).strftime('%d.%m.%Y %H:%M')}\n\n⚠️ Muddatdan keyin avtomatik o'chadi", 
            parse_mode="HTML", 
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Asosiy Menyuga", callback_data="main")]
            ])
        )
    except Exception as e:
        await processing.edit_text(f"❌ Xatolik: {str(e)[:100]}", reply_markup=get_main_menu())
    
    await cb.answer()

# ADMIN COMMANDS
@dp.message(Command("stats"))
async def stats_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("⛔️ Bu komanda faqat admin uchun!")
        return
    
    total_users = len(user_channels)
    total_channels = sum(len(ch) for ch in user_channels.values())
    
    # Eng ko'p kanal qo'shgan foydalanuvchi
    top_user = max(user_channels.items(), key=lambda x: len(x[1])) if user_channels else (0, [])
    
    stats_text = f"""
📊 <b>BOT STATISTIKASI</b>

👥 <b>Jami foydalanuvchilar:</b> {total_users:,}
📢 <b>Jami kanallar:</b> {total_channels:,}
📈 <b>O'rtacha:</b> {total_channels/total_users if total_users > 0 else 0:.1f} kanal/user

🏆 <b>Top foydalanuvchi:</b>
   User ID: <code>{top_user[0]}</code>
   Kanallar: {len(top_user[1])} ta

💾 <b>Ma'lumotlar bazasi:</b> {os.path.getsize(DATA_FILE) if os.path.exists(DATA_FILE) else 0:,} bayt
📋 <b>Loglar hajmi:</b> {os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0:,} bayt

🤖 <b>Bot holati:</b> ✅ Aktiv
⏰ <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
"""
    
    await msg.answer(stats_text, parse_mode="HTML")

@dp.message(Command("logs"))
async def logs_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("⛔️ Bu komanda faqat admin uchun!")
        return
    
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
            await msg.answer_document(
                FSInputFile(LOG_FILE), 
                caption=f"📋 <b>Faoliyat Jurnali</b>\n\n📊 Hajm: {os.path.getsize(LOG_FILE):,} bayt\n📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}", 
                parse_mode="HTML"
            )
        else:
            await msg.answer("📭 <b>Loglar fayli bo'sh!</b>", parse_mode="HTML")
    except Exception as e:
        await msg.answer(f"❌ Xatolik: {str(e)}")

@dp.message(Command("backup"))
async def backup_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("⛔️ Bu komanda faqat admin uchun!")
        return
    
    try:
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            await msg.answer_document(
                FSInputFile(DATA_FILE), 
                caption=f"💾 <b>Ma'lumotlar Bazasi Zaxirasi</b>\n\n👥 Foydalanuvchilar: {len(user_channels)}\n📢 Kanallar: {sum(len(ch) for ch in user_channels.values())}\n📊 Hajm: {os.path.getsize(DATA_FILE):,} bayt\n📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}", 
                parse_mode="HTML"
            )
        else:
            await msg.answer("📭 <b>Ma'lumotlar bazasi bo'sh!</b>", parse_mode="HTML")
    except Exception as e:
        await msg.answer(f"❌ Xatolik: {str(e)}")

@dp.message(Command("broadcast"))
async def broadcast_cmd(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("⛔️ Bu komanda faqat admin uchun!")
        return
    
    # Broadcast xabar yuborish
    if len(msg.text.split(maxsplit=1)) < 2:
        await msg.answer("❌ <b>Format:</b> /broadcast Xabar matni", parse_mode="HTML")
        return
    
    text = msg.text.split(maxsplit=1)[1]
    success = 0
    failed = 0
    
    status_msg = await msg.answer("📤 <b>Xabar yuborilmoqda...</b>", parse_mode="HTML")
    
    for user_id in user_channels.keys():
        try:
            await bot.send_message(user_id, f"📢 <b>ADMIN XABARI</b>\n\n{text}", parse_mode="HTML")
            success += 1
            await asyncio.sleep(0.05)  # Anti-flood
        except:
            failed += 1
    
    await status_msg.edit_text(
        f"✅ <b>Broadcast Yakunlandi!</b>\n\n✅ Muvaffaqiyatli: {success}\n❌ Xatolik: {failed}\n📊 Jami: {success + failed}", 
        parse_mode="HTML"
    )

# UNKNOWN MESSAGES
@dp.message()
async def unknown_msg(msg: Message):
    await msg.answer(
        "❓ <b>Noma'lum Komanda</b>\n\nBotni ishga tushirish uchun /start ni bosing", 
        parse_mode="HTML", 
        reply_markup=get_main_menu()
    )

# STARTUP & SHUTDOWN
async def on_startup():
    print("=" * 50)
    print("🚀 BOT MUVAFFAQIYATLI ISHGA TUSHDI!")
    print(f"📊 Foydalanuvchilar: {len(user_channels)}")
    print(f"📢 Jami kanallar: {sum(len(ch) for ch in user_channels.values())}")
    print(f"⏰ Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print("=" * 50)
    
    try:
        await bot.send_message(
            ADMIN_ID, 
            f"✅ <b>Bot Ishga Tushdi!</b>\n\n📊 Foydalanuvchilar: {len(user_channels)}\n📢 Kanallar: {sum(len(ch) for ch in user_channels.values())}\n⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", 
            parse_mode="HTML"
        )
    except:
        pass

async def on_shutdown():
    print("\n" + "=" * 50)
    print("🛑 BOT TO'XTATILDI!")
    print(f"⏰ Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print("=" * 50)
    
    save_data(user_channels)
    
    try:
        await bot.send_message(
            ADMIN_ID, 
            f"🛑 <b>Bot To'xtatildi!</b>\n\n⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", 
            parse_mode="HTML"
        )
    except:
        pass

# MAIN FUNCTION
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        print("⏳ Bot ishga tushmoqda...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Bot Ctrl+C bilan to'xtatildi!")
    except Exception as e:
        print(f"\n❌ KRITIK XATOLIK: {e}")
        import traceback
        traceback.print_exc()