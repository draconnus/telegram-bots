__author__ = 'Darko'
from telegram import Updater, Message
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("../global.settings")
token = config.get("GameOrganizerSection", "odbojka_bot_token")
updater = Updater(token=token)
dispatcher = updater.dispatcher

clients = []
users = []
accepted = []
declined = []

command_list = "Raspolozive komande:\n" \
           "/start\n" \
           "/list\n" \
           "/list\n" \
           "/da\n" \
           "/ne\n" \
           "/ko_dolazi\n" \
           "/ko_ne_dolazi\n"

def start(bot, update):
    user_id = update.message.chat_id
    if find_user(user_id, users) is None:
        user = {
            "chat_id": user_id,
            "name": update.message.chat.name,
            "last_name": update.message.chat.last_name
        }
        users.append(user)

        clients.append(user_id)
    bot.sendMessage(chat_id=user_id, text="I'm a bot dude!")

def not_recognized():
    return "Niste se registrovali. Registruj se sa \n/start komandom"

def find_user(user_id, user_list):
    return next((x for x in user_list if x["chat_id"] == user_id), None)

def remove_from_list(user_id, user_list):
    user_list.remove(next((x for x in users if x["chat_id"] == user_id), None))

def accept(bot, update):
    user_id = update.message.chat_id
    user = find_user(user_id, users)
    if  user is None:
        bot.sendMessage(chat_id=user_id, text=not_recognized())
        return
    accepted.append(user)
    if find_user(user_id, declined) is not None:
        remove_from_list(user_id, declined)

def decline(bot, update):
    user_id = update.message.chat_id
    user = find_user(user_id, users)
    if user is None:
        bot.sendMessage(chat_id=user_id, text=not_recognized())
        return
    declined.append(user)
    if find_user(user_id, accepted) is not None:
        remove_from_list(update.message.chat_id, accepted)

def get_all_participants(bot, update):
    participants = (", ").join("{} {}".format(x["name"], x["last_name"]) for x in users)
    participants_text = "Registrovani ({}): {}".format(len(users), participants)
    bot.sendMessage(chat_id=update.message.chat_id, text=participants_text)

def get_accepted_participants(bot, update):
    participants = (", ").join("{} {}".format(x["name"], x["last_name"]) for x in accepted)
    participants_text = "Potvrdili dolazak ({}): {}".format(len(accepted), participants)
    bot.sendMessage(chat_id=update.message.chat_id, text=participants_text)

def get_declined_participants(bot, update):
    participants = (", ").join("{} {}".format(x["name"], x["last_name"]) for x in declined)
    participants_text = "Rekli da ne dolaze ({}): {}".format(len(declined), participants)
    bot.sendMessage(chat_id=update.message.chat_id, text=participants_text)

def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=command_list)

dispatcher.addTelegramCommandHandler('start', start)
dispatcher.addTelegramCommandHandler('list', get_all_participants)
dispatcher.addTelegramCommandHandler('help', help)
dispatcher.addTelegramCommandHandler('da', accept)
dispatcher.addTelegramCommandHandler('ne', decline)
dispatcher.addTelegramCommandHandler('ko_dolazi', get_accepted_participants)
dispatcher.addTelegramCommandHandler('ko_ne_dolazi', get_declined_participants)
dispatcher.addUnknownTelegramCommandHandler(help)

updater.start_polling()
