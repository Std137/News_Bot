from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.types.callback_query import CallbackQuery

class Views():
	'''
	Основной обработчик сообщений
	'''
	
	def __init__(self, config, bot, u_data):
		self.keyboard_set = config.get()['fsm_message']
		self.chat_set = config.get()['Chat_Preferences']
		self.keyboard_complite = {}
		self.bot = bot
		self.u_data = u_data
		for section in self.keyboard_set.keys():
			section_data = self.keyboard_set[section]
			keyboard_line = []
			for section_keys in section_data.keys():
				button_line = []
				if section_keys == 'text': 
					section_caption = section_data['text']
				else:
					line_data = section_data[section_keys]
					for key in line_data.keys():
						button_line.append(InlineKeyboardButton(text=line_data[key]['text'], callback_data =line_data[key]['callback']))
				if len(button_line) != 0:
					keyboard_line.append(button_line)
			keyboard_section = InlineKeyboardMarkup(inline_keyboard=keyboard_line)
			self.keyboard_complite[section] = {'text':section_caption, 'key':keyboard_section}

	async def sendtext(self, message, item = None):
		u_id = message.from_user.id
		u_name = message.from_user.username
		if (self.u_data[u_id]['u_fsm'] == 7) and (item == None):
			await self.sendpreview(message, u_id, u_name)
		if item == None:
			item = str(self.u_data[u_id]['u_fsm'])
		response = self.keyboard_complite[item]['text'].format(u_name)
		await message.answer(response, reply_markup = self.keyboard_complite[item]['key'], parse_mode=ParseMode.HTML)

	async def resetkey(self, callback):
		await callback.message.edit_reply_markup(reply_markup=None)

	async def sendresult(self, message):
		self.chat_set = config.get()['Chat_Preferences']
		username = message.from_user.username
		u_id = message.from_user.id
		if (isinstance(message, CallbackQuery)):
			message = message.message
		text_msg = self.CreateResultatMessage(self.u_data[u_id], username)
		if self.u_data[u_id]['msg_pic'] == '':
			for chat in self.chat_set['chat_id']:
				await self.bot.send_message(chat_id = chat, text = text_msg, parse_mode=ParseMode.HTML)
		else:
			for chat in self.chat_set['chat_id']:
				await self.bot.send_photo(chat_id = chat, photo = self.u_data[u_id]['msg_pic'], caption=text_msg,  parse_mode=ParseMode.HTML)

	async def sendpreview(self, message, u_id, u_name):
		text_msg = self.CreateResultatMessage(self.u_data[u_id], u_name)
		if self.u_data[u_id]['msg_pic'] == '':
			await message.answer(text_msg, parse_mode=ParseMode.HTML)
		else:
			await message.answer_photo(self.u_data[u_id]['msg_pic'], caption = text_msg,  parse_mode=ParseMode.HTML)

	def CreateResultatMessage(self, senddata, username):
		msg_sep = '==='
		if senddata['msg_about'] != '':
			msg_ab = f"\n{senddata['msg_about']}\n\n"
		else:
			msg_ab = ""
		if senddata['msg_date'] != '':
			msg_dt = f"Дата мероприятия:\n{senddata['msg_date']}\n Время мероприятия:\n{senddata['msg_time']}(MCK) \n"
		else:
			msg_dt = ""
		send_msg = f"<b><i>{senddata['msg_header']}</i></b>\n{msg_ab}{msg_dt}{msg_sep}\nПодробности:\n<a>{senddata['msg_link']}</a>{msg_sep}\n<i>Поделился @{username},\nчерез бота <a href = \'http://telegram.me/FPGA_news_post_bot?start=start\'> @FPGA_news_post_bot.</a></i>"
		return send_msg
