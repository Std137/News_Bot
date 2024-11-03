from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from datetime import datetime

class Router_Message(Router):
    def __init__(self, user_data, config, views, filters):
        super().__init__()
        self.user_data = user_data
        self.send = views
        self.message.register(self.accepted_data, F.text, filters.What_Received(self.user_data, 1))
        self.message.register(self.accepted_time, F.text, filters.What_Received(self.user_data, 2))
        self.message.register(self.accepted_link, F.text, filters.What_Received(self.user_data, 3))
        self.message.register(self.accepted_header, F.text, filters.What_Received(self.user_data, 4))
        self.message.register(self.accepted_about, F.text, filters.What_Received(self.user_data, 5))
        self.message.register(self.accepted_pic, F.photo, filters.What_Received(self.user_data, 6))
        self.message.register(self.accepted_edit, F.text, filters.What_Received(self.user_data, 8))
        self.message.register(self.accepted_err, filters.Other(self.user_data))

#1
    async def accepted_data(self, message):
        u_load = self.user_data[message.from_user.id]
        try:
            enter_date = datetime.strptime(message.text, '%d.%m.%Y').date()
            if enter_date > datetime.today().date():
                u_load['msg_date'] = enter_date.strftime('%d.%m.%Y')
                self.user_data[message.from_user.id] = u_load
                self.user_data.next_state(message.from_user.id, 2)
                await self.send.sendtext(message)
            else:
                await self.send.sendtext(message,'senderrordate')
        except ValueError:
            await self.send.sendtext(message,'senderrordate')
#2
    async def accepted_time(self, message):
        u_load = self.user_data[message.from_user.id]
        try:
            enter_time = datetime.strptime(message.text,'%H:%M').time()
            u_load['msg_time'] = enter_time.strftime('%H:%M')
            self.user_data[message.from_user.id] = u_load
            self.user_data.next_state(message.from_user.id, 3)
            await self.send.sendtext(message)
        except ValueError:
            await self.send.sendtext(message,'senderrortime')
#3
    async def accepted_link(self, message):
        u_load = self.user_data[message.from_user.id]
        u_load['msg_link'] = ''
        url = []
        try:
            entities = message.entities
            if entities == None:
                entities = []
            for item in entities:
                if item.type == 'url':
                    link = item.extract_from(message.text).lower()
                    if (link[0] != 'h'):
                        link = 'http://' + link
                    u_load['msg_link'] = u_load['msg_link'] + link + '\n'
            if u_load['msg_link'] != '':
                self.user_data[message.from_user.id] = u_load
                self.user_data.next_state(message.from_user.id, 4)
                await self.send.sendtext(message)
            else:
                await self.send.sendtext(message, 'senderrorlink')
        except ValueError:
            await self.send.sendtext(message,'senderrorlink')
#4

    async def accepted_header(self, message):
        u_load = self.user_data[message.from_user.id]
        try:
            u_load['msg_header'] = message.text
            self.user_data[message.from_user.id] = u_load
            self.user_data.next_state(message.from_user.id, 5)
            await self.send.sendtext(message)
        except ValueError:
            await self.send.sendtext(message,'senderror')

#5
    async def accepted_about(self, message):
        u_load = self.user_data[message.from_user.id]
        try:
            u_load['msg_about'] = message.text
            self.user_data[message.from_user.id] = u_load
            self.user_data.next_state(message.from_user.id, 6)
            await self.send.sendtext(message)
        except ValueError:
            await self.send.sendtext(message,'senderror')

#6 Обработчик 6 шаг. Проверяет картинку
    async def accepted_pic(self, message):
        u_load = self.user_data[message.from_user.id]
        try:
            u_load['msg_pic'] = message.photo[0].file_id
            self.user_data[message.from_user.id] = u_load
            self.user_data.next_state(message.from_user.id, 7)
            await self.send.sendtext(message)
        except ValueError:
            await self.send.sendtext(message,'senderrorload')

#7 Обработчик 7 шаг. Выбор режима редактирования.
    async def accepted_edit(self, message):
        u_load = self.user_data[message.from_user.id]
        try:
            edit_step = str(message.text)
            if edit_step in ['1','2','3','4','5','6']:
                self.user_data[message.from_user.id] = u_load
                self.user_data.next_state(message.from_user.id, int(edit_step))
                await self.send.sendtext(message, str(edit_step))
            else:
                await self.send.sendtext(message,'senderror')
        except ValueError:
            await self.send.sendtext(message,'senderror')


#Последний хандлер. Отрабатывает если не сработали другие хандлеры

    async def accepted_err(self, message):
        await self.send.sendtext(message,'senderror')
