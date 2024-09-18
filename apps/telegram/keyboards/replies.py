from telegram import KeyboardButton, ReplyKeyboardMarkup

def get_contact():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("Telefon raqamni yuborish", request_contact=True)
            ]
        ], resize_keyboard=True
    )

def get_gender():
    return ReplyKeyboardMarkup(


        [
            [
                KeyboardButton("Erkak"), KeyboardButton("Ayol")


            ]
        ], resize_keyboard=True
    )

def get_items(items, key):
    keyboards = []
    for item in items:
        keyboards.append(
            [
            KeyboardButton(
                getattr(item, key)
            )
                ]
        )
    return ReplyKeyboardMarkup(
        keyboards, resize_keyboard=True
    )