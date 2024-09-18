from apps.telegram.models import TelegramUser
from apps.telegram.keyboards import replies
from apps.telegram import states

def start(update, context):
    user=update.message.from_user
    first_name=user.first_name
    last_name = user.last_name
    telegram_id = user.id

    TelegramUser.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={
            "last_name":last_name,
            "first_name":first_name
        }

    )
    message="Assalomu aleykum, TIFT.uz botiga xush kelibsiz iltimos telefon raqamingizni yuboring."
    update.message.reply_text(message, reply_markup=replies.get_contact())
    return states.PHONE
def help(update, context):
    update.message.reply_text("Yordam")