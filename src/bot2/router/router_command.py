from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

class Router_Command(Router):
    def __init__(self, user_data, config, views, filters):
        super().__init__()
        self.user_data = user_data
        self.send = views
        self.config = config
        self.message.register(self.add_chat, Command(commands=["add"]), filters.IsAdmin())
        self.message.register(self.del_chat, Command(commands=["del"]), filters.IsAdmin())
        self.message.register(self.block_user, Command(commands=["block"]), filters.IsAdmin())
        self.message.register(self.unblock_user, Command(commands=["unblock"]), filters.IsAdmin())
        self.message.register(self.control_private, filters.IsPrivate())
        self.message.register(self.control_block, filters.IsBlock(self.user_data))
        self.message.register(self.helper, Command(commands=["help"]))
        self.message.register(self.start_new, Command(commands=["start"]), filters.IsNew(self.user_data))
        self.message.register(self.start_old, Command(commands=["start"]), filters.IsOld(self.user_data))

    async def control_private(self, message):
        await self.send.sendtext(message,'sendinvite')

    async def control_block(self, message):
        await self.send.sendtext(message,'sendblock')

    async def helper(self, message):
        await self.send.sendtext(message,'sendhelp')

    async def start_new(self, message):
        await self.send.sendtext(message, '0')

    async def start_old(self, message):
        await self.send.sendtext( message, 'old')

    async def add_chat(self, message):
        chst = self.config.get()
        test = str(message.chat.id)
        if test in chst['Chat_Preferences']['chat_id']:
            await self.send.sendtext( message, 'add_chat_err')
        else:
            chst['Chat_Preferences']['chat_id'].append(test)
            self.config.set(chst)
            await self.send.sendtext( message, 'add_chat')

    async def del_chat(self, message):
        chst = self.config.get()
        test = str(message.chat.id)
        new_line = set(chst['Chat_Preferences']['chat_id'])
        if test in new_line:
            new_line.discard(test)
            chst['Chat_Preferences']['chat_id'] = list(new_line)
            print (new_line)
            self.config.set(chst)
            await self.send.sendtext( message, 'del_chat')
        else:
            await self.send.sendtext( message, 'del_chat_err')
        

    async def block_user(self, message, command):
        if message.reply_to_message != None:
            id_user = str(message.reply_to_message.from_user.id)
            save = self.user_data[int(id_user)]
            save['u_block'] = 1
            self.user_data[int(id_user)] = save
            await self.send.sendtext(message, 'block_user')
        else:
            await self.send.sendtext(message, 'block_user_err')

    async def unblock_user(self, message, command):
        u_unblock_id = command.args
        if u_unblock_id != None:
            save = self.user_data[int(u_unblock_id)]
            save['u_block'] = 0
            self.user_data[int(u_unblock_id)] = save
            await self.send.sendtext( message, 'unblock_user')
        else:    
            await self.send.sendtext( message, 'unblock_err')
