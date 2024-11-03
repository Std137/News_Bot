from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsNews(BaseFilter):
    def __init__(self):
        self.chat_type = 'private'

    async def __call__(self, message):
        return message.chat.type != self.chat_type
