from aiogram import Router, F
from aiogram.types import Message
import json


class Router_Keyboard(Router):
    def __init__(self, user_data, config, views, filters):
        super().__init__()
        self.user_data = user_data
        self.send = views
        self.config = config
        self.callback_query.register(self.select_next_3, F.data.in_({"news", "resurs"}))
        self.callback_query.register(self.select_next_1, F.data.in_({"online", "offline"}))
        self.callback_query.register(self.skip_about, F.data == "skip_about")
        self.callback_query.register(self.add_about, F.data == "add_about")
        self.callback_query.register(self.skip_pic, F.data == "skip_pic")
        self.callback_query.register(self.add_pic, F.data == "add_pic")
        self.callback_query.register(self.select_continue, F.data == "continue")
        self.callback_query.register(self.select_reset, F.data == "restart")
        self.callback_query.register(self.sendinchat, F.data == "sendinchat")
        self.callback_query.register(self.editmode, F.data == "editmode")


    async def select_next_3(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        self.user_data.next_state(u_id, 3)
        await self.send.resetkey(callback)
        await self.send.sendtext(callback)

    async def select_next_1(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        self.user_data.next_state(u_id, 1)
        await self.send.resetkey(callback)
        await self.send.sendtext(callback)

    async def skip_about(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        self.user_data.next_state(u_id, 6)
        await self.send.resetkey(callback)
        await self.send.sendtext(callback)

    async def add_about(self, callback):
        u_id = callback.from_user.id
        await self.send.resetkey(callback)

    async def skip_pic(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        self.user_data.next_state(u_id, 7)
        await self.send.resetkey(callback)
        await self.send.sendtext(callback)

    async def add_pic(self, callback):
        await self.send.resetkey(callback)

    async def select_continue(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        await self.send.resetkey(callback)
        await self.send.sendtext(callback)

    async def select_reset(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        await self.send.resetkey(callback)
        self.user_data.next_state(u_id, 0)
        await self.send.sendtext(callback)

    async def send_result(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        await self.send.resetkey(callback)
        await self.send.sendtext(callback)

    async def sendinchat(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        await self.send.resetkey(callback)
        await self.send.sendresult(callback)
        self.user_data.msg_finish(u_id)
        self.user_data.next_state(u_id, 0)
        await self.send.sendtext(callback, 'sendstatusok')

    async def editmode(self, callback):
        u_id = callback.from_user.id
        u_name = callback.from_user.username
        await self.send.resetkey(callback)
        self.user_data.next_state(u_id, 8)
        await self.send.sendtext(callback)
