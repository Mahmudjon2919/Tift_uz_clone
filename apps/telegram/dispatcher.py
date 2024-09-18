import telegram
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler
from apps.telegram import states
from apps.telegram.handlers import commands, common, registration
from django.conf import settings

bot = Bot(token=settings.BOT_TOKEN)


dispatcher = Dispatcher(bot, None, workers=0)

dispatcher.add_handler(
    ConversationHandler(
        entry_points=[CommandHandler("start", commands.start)],
        states={
            states.PHONE:[MessageHandler(Filters.all, registration.get_phone)],
            states.FULL_NAME:[MessageHandler(Filters.all, registration.get_full_name)],
            states.PASSPORT:[MessageHandler(Filters.all, registration.get_passport)],
            states.GENDER:[MessageHandler(Filters.all, registration.get_gender)],
            states.PINFIL:[MessageHandler(Filters.all, registration.get_pinfil)],
            states.BIRTH_DATA:[MessageHandler(Filters.text, registration.get_birth_date)],
            states.FACULTY:[MessageHandler(Filters.text, registration.get_faculty)],
            states.DIRECTION:[MessageHandler(Filters.text, registration.get_direction)],
            states.REGION:[MessageHandler(Filters.text, registration.get_region)],
            states.DISTRICT:[MessageHandler(Filters.text, registration.get_district)],

        },
        fallbacks=[CommandHandler("start", commands.start)]
    )
)

dispatcher.add_handler((CommandHandler("help", commands.help)))
dispatcher.add_handler(MessageHandler(Filters.all, common.echo))