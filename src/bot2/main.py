import pathlib
import logging
import sys
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from os import getenv
from setup import Setup
from module.model import User_Data
from view.views import Views
import filter.filters_command as filters
from router.router_command import Router_Command
from router.router_keyboard import Router_Keyboard
from router.router_message import Router_Message
import signal


#Initialization of constants
config_init = Setup()
TOKEN = getenv("BOT_TOKEN")
PATHDB = pathlib.Path(__file__).parent / config['Database']['name']
WEB_SERVER_HOST = config['Web_Init']['host']
WEB_SERVER_PORT = config['Web_Init']['port']
WEBHOOK_PATH = config['Web_Init']['path']
WEBHOOK_SECRET = config['Web_Init']['secret']
BASE_WEBHOOK_URL = config['Web_Init']['url']

#Initialization of modules
bot = Bot(TOKEN)
user_data = User_Data(PATHDB)
views = Views(config_init, config['fsm_message'], config['Chat_Preferences'], bot, user_data)
router_comands_add = Router_Command(user_data, config_init, views, filters)
router_keyboard_add = Router_Keyboard(user_data, config, views, filters)
router_message_add = Router_Message(user_data, config, views, filters)

def receiveSignal(signalNumber, frame):
 if signalNumber.sig

async def on_startup(bot):
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

def main():
    dp = Dispatcher()
    dp.include_router(router_comands_add)
    dp.include_router(router_keyboard_add)
    dp.include_router(router_message_add)
    dp.startup.register(on_startup)
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    signal.signal(signal, receiveSignal) 
    main()