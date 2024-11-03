from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPrivate(BaseFilter):
    def __init__(self):
        self.chat_type = 'private'

    async def __call__(self, message):
        return message.chat.type != self.chat_type

class IsBlock(BaseFilter):
    def __init__(self, user_data):
        self.user_data = user_data

    async def __call__(self, message):
        return self.user_data[message.from_user.id]['u_block'] == 1
         
class IsNew(BaseFilter):
    def __init__(self, user_data):
        self.user_data = user_data

    async def __call__(self, message):
        return self.user_data[message.from_user.id]['u_fsm'] == 0

class IsOld(BaseFilter):
    def __init__(self, user_data):
        self.user_data = user_data

    async def __call__(self, message):
        return self.user_data[message.from_user.id]['u_fsm'] != 0

class What_Received(BaseFilter):
    def __init__(self, user_data, fsm_state):
        self.user_data = user_data
        self.fsm_state = fsm_state

    async def __call__(self, message):
        return self.user_data[message.from_user.id]['u_fsm'] == self.fsm_state

class Other(BaseFilter):
    def __init__(self, user_data):
        self.user_data = user_data

    async def __call__(self, message):
        return 5==5

class IsAdmin(BaseFilter):
    def __init__(self):
        self.admin_id = '1607286706'

    async def __call__(self, message):
        return str(message.from_user.id) == self.admin_id
