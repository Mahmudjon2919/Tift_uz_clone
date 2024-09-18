
from apps.application.models import Application
from apps.telegram.keyboards import replies
from apps.telegram import states
from telegram import ReplyKeyboardRemove
import re
from datetime import datetime
from apps.education.models import Faculty, Direction
from apps.common.models import Region, District


def get_phone(update, context):
    if update.message and update.message.contact:
        contact_user_id = update.message.contact.user_id
        user_id = update.message.from_user.id

        if Application.objects.filter(user_id=user_id).exists():
            update.message.reply_text(
                "You have already submitted your application and cannot resubmit it.",
                reply_markup=ReplyKeyboardRemove()
            )
            return states.END

        if contact_user_id != user_id:
            update.message.reply_text("This number does not belong to you!", reply_markup=replies.get_contact())
            return states.PHONE

        phone = update.message.contact.phone_number
        context.user_data['phone'] = phone
        update.message.reply_text("You are in the tight way, Send your full name ", reply_markup=ReplyKeyboardRemove())
        return states.FULL_NAME
    update.message.reply_text("Please send your phone number by button!", reply_markup=replies.get_contact())
    return states.PHONE


def get_full_name(update, context):
    if update.message and update.message.text:
        full_name = update.message.text
        context.user_data['full_name'] = full_name
        update.message.reply_text("Everything is ok, send your passport in AA1234567 format",
                                  reply_markup=ReplyKeyboardRemove())
        return states.PASSPORT

    update.message.reply_text("Please your name as text", reply_markup=ReplyKeyboardRemove())
    return states.FULL_NAME


def get_passport(update, context):
    if update.message and update.message.text:
        if re.match("^[A-Z]{2}\d{7}$", update.message.text):
            context.user_data['passport'] = update.message.text
            update.message.reply_text("Correct, please send your pinfl")
            return states.PINFIL

    update.message.reply_text("Please send your passport in AA1234567 format",
                              reply_markup=ReplyKeyboardRemove())
    return states.PASSPORT


def get_pinfil(update, context):
    if update.message and update.message.text:
        if re.match("^\d{14}$", update.message.text):
            context.user_data['pinfl'] = update.message.text
            update.message.reply_text("Correct, please send your gender", reply_markup=replies.get_gender())
            return states.GENDER
    update.message.reply_text("Please send your pinfl data in 14 digits",
                              reply_markup=ReplyKeyboardRemove())
    return states.PINFL


def get_gender(update, context):
    if update.message and update.message.text:
        text = update.message.text
        genders = {
            "Erkak": "male",
            "Ayol": "female",
        }
        if text in genders.keys():
            context.user_data["gender"] = genders[text]
            update.message.reply_text("Please send your birth date in (DD.MM.YYYY) format",
                                      reply_markup=ReplyKeyboardRemove())
            return states.BIRTH_DATA

    update.message.reply_text("Please choose your gender through the buttons below",
                              reply_markup=replies.get_gender())
    return states.GENDER


def get_birth_date(update, context):
    if update.message and update.message.text:
        text = update.message.text
        if re.match("^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(199[5-9]|20[0-1][0-9]|202[0-4])$", text):
            try:
                birth_date = datetime.strptime(text, '%d.%m.%Y')
                context.user_data['birth_date'] = birth_date
                update.message.reply_text("Correct, please send your faculty",
                                          reply_markup=replies.get_items(Faculty.objects.all(), "title"))

                return states.FACULTY
            except ValueError:
                pass


        update.message.reply_text("Please send your birth date in (DD.MM.YYYY) format", reply_markup=ReplyKeyboardRemove())
        return states.BIRTH_DATE


def get_faculty(update, context):
    if update.message and update.message.text:
        text = update.message.text
        try:
            faculty = Faculty.objects.get(title=text)
            context.user_data['faculty'] = faculty.id
            update.message.reply_text(
                "Please choose your direction",
                reply_markup=replies.get_items(faculty.directions.all(), "title")
            )
            return states.DIRECTION
        except Faculty.DoesNotExist:
            update.message.reply_text(
                "The selected faculty does not exist. Please choose a valid faculty from the list.",
                reply_markup=replies.get_items(Faculty.objects.all(), "title")
            )
            return states.FACULTY

    update.message.reply_text(
        "Please send your faculty by choosing from the list below.",
        reply_markup=replies.get_items(Faculty.objects.all(), "title")
    )
    return states.FACULTY


def get_direction(update, context):
    if update.message and update.message.text:
        text = update.message.text
        faculty_id = context.user_data.get('faculty')

        try:
            faculty = Faculty.objects.get(id=faculty_id)
            direction = faculty.directions.get(title=text)
            context.user_data['directions'] = direction.id
            update.message.reply_text(
                "Please choose your region",
                reply_markup=replies.get_items(Region.objects.all(), "title")
            )
            return states.REGION
        except Faculty.DoesNotExist:
            update.message.reply_text(
                "The selected faculty does not exist. Please try again.",
                reply_markup=replies.get_items(Faculty.objects.all(), "title")
            )
            return states.FACULTY
        except Direction.DoesNotExist:
            update.message.reply_text(
                "The selected direction is not valid. Please choose a valid direction.",
                reply_markup=replies.get_items(faculty.directions.all(), "title")
            )
            return states.DIRECTION

    update.message.reply_text(
        "Please choose your direction from the available options.",
        reply_markup=replies.get_items(Faculty.objects.get(id=context.user_data['faculty']).direction.all(), "title")
    )
    return states.DIRECTION


def get_region(update, context):
    if update.message and update.message.text:
        text = update.message.text
        try:
            region = Region.objects.get(title=text)
            context.user_data['region'] = region.id

            update.message.reply_text(
                "Please select your district",
                reply_markup=replies.get_items(region.districts.all(), "title")
            )
            return states.DISTRICT
        except Region.DoesNotExist:
            update.message.reply_text(
                "The selected region does not exist. Please choose a valid region from the list.",
                reply_markup=replies.get_items(Region.objects.all(), "title")
            )
            return states.REGION

    update.message.reply_text(
        "Please choose your region.",
        reply_markup=replies.get_items(Region.objects.all(), "title")
    )
    return states.REGION


def get_district(update, context):
    if update.message and update.message.text:
        text = update.message.text
        try:
            district = District.objects.get(title=text)
            context.user_data['district'] = district.id
            update.message.reply_text(
                "Registration complete! Your information has been saved. \n\n"
                "Hello TFIT.uz welcome to boti send your phone number to leave an application",
                reply_markup=replies.get_contact()
            )
            return states.PHONE
        except District.DoesNotExist:
            region = Region.objects.get(id=context.user_data['region'])
            update.message.reply_text(
                "District not found. Please choose a valid district.",
                reply_markup=replies.get_items(region.districts.all(), "title")
            )
            return states.DISTRICT

    region = Region.objects.get(id=context.user_data['region'])
    update.message.reply_text(
        "Please choose your district.",
        reply_markup=replies.get_items(region.districts.all(), "title")
    )
    return states.DISTRICT