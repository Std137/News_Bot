from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message


class What_Received(BaseFilter):
    def __init__(self):

    async def __call__(self, fsm, fsm_state):
        return fsm['u_fsm'] == state
