# -*- coding: utf-8 -*-
import telebot.util
from telebot import types
import operator


# Configuration ######################################################
bot = telebot.TeleBot('452287428:AAGZN3UERRMHScNzD6tK6IG9h_6AB_HXglY')

owner_id = ''
######################################################################


lean_coffee = dict()
themes = set()


@bot.message_handler(commands=['lean'])
def lean(message):
    global lean_coffee
    global themes
    global owner_id

    lean_coffee = {}
    themes = set()

    owner_id = message.chat.id
    lean_coffee[str(owner_id)] = {}
    bot.send_message(message.chat.id, "Lean has started, you are an owner")


@bot.message_handler(commands=['signup'])
def register(message):
    lean_coffee[str(message.chat.id)] = {}
    bot.send_message(message.chat.id, "You are registered for participation in lean coffee")


@bot.message_handler(commands=['raise'])
def raise_theme(message):
    global lean_coffee
    global themes

    chat_id = str(message.chat.id)
    if chat_id not in lean_coffee.keys():
        lean_coffee[chat_id] = {}

    theme = message.text.replace("/raise", "").strip()
    if theme:
        themes.add(theme)
        bot.send_message(message.chat.id,
                         message.chat.first_name + ' ' + message.chat.last_name + ' raise theme "' + theme + '"')
    else:
        bot.send_message(message.chat.id,
                         'Raised theme cannot be empty')


@bot.message_handler(commands=['decline'])
def decline_theme(message):
    global themes

    theme = message.text.replace("/decline", "").strip()
    if theme:
        themes.discard(theme)
        bot.send_message(message.chat.id,
                         message.chat.first_name + ' ' + message.chat.last_name + ' decline theme "' + theme + '"')
    else:
        bot.send_message(message.chat.id,
                         'Declined theme cannot be empty')


@bot.message_handler(commands=['vote'])
def vote(message):
    global lean_coffee

    if message.chat.id == owner_id:
        markup = types.ReplyKeyboardMarkup(row_width=1)

        for theme in sorted(themes):
            for participant in lean_coffee.keys():
                lean_coffee[participant][theme] = False
            markup.add(types.KeyboardButton('Vote for: ' + theme))

        for participant in lean_coffee.keys():
            bot.send_message(participant, 'Vote started', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Vote operation allowed for owner only')


@bot.message_handler(commands=['stop'])
def stop(message):
    global lean_coffee

    if message.chat.id == owner_id:

        results = {}
        for key in lean_coffee.keys():
            for theme in lean_coffee[key].keys():
                if theme in results.keys():
                    results[theme] += 1 if lean_coffee[key][theme] else 0
                else:
                    results[theme] = 1 if lean_coffee[key][theme] else 0
        themes_result = '\n'.join([i[0] for i in sorted(results.items(), key=operator.itemgetter(1), reverse=True)])

        # store to excel

        markup = types.ReplyKeyboardRemove()
        for participant in lean_coffee.keys():
            bot.send_message(participant, 'Vote stopped', reply_markup=markup)
            bot.send_message(participant, 'Themes:\n' + themes_result)
    else:
        bot.send_message(message.chat.id, 'Stop operation allowed for owner only')


@bot.message_handler(commands=['print'])
def help(message):
    global participants
    global themes

    bot.send_message(message.chat.id, 'Participants: ' + ', '.join(participants))
    bot.send_message(message.chat.id, 'Themes: \n' + '\n'.join(themes))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def text(message):
    vote_key = 'Vote for: '
    unvote_key = 'Unvote for: '

    if message.text.startswith(vote_key) or message.text.startswith(unvote_key):

        if message.text.startswith(vote_key):
            lean_coffee[str(message.chat.id)][message.text[len(vote_key):]] = True
        elif message.text.startswith(unvote_key):
            lean_coffee[str(message.chat.id)][message.text[len(unvote_key):]] = False

        votes = lean_coffee[str(message.chat.id)]

        markup = types.ReplyKeyboardMarkup(row_width=1)
        for theme in votes.keys():
            markup.add(types.KeyboardButton((unvote_key if votes[theme] else vote_key) + theme))

        bot.send_message(message.chat.id, 'Vote changed', reply_markup=markup)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except BaseException:
        print 'Connection refused'
