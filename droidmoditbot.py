import sqlite3

import telebot
from telebot import *

from config import *

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('botdm.db', check_same_thread=False)
c = conn.cursor()

# idk why
currpostid = 2
currpostidg = 1

# dizionario per il flood
flood = dict()

try:
    c.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, username TEXT)")  # create table users
except Exception as e:
    print(e)
try:
    c.execute("CREATE TABLE IF NOT EXISTS warns(user_id INTEGER, warn INTEGER)")  # create table warns
except Exception as e:
    print(e)


# start command
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Canale", url="https://telegram.me/moditchan"))
    markup.add(types.InlineKeyboardButton("Gruppo", url="https://telegram.me/androidmoddingitalia"))
    if message.chat.id in officialchats:
        return
    else:
        try:
            bot.send_message(message.from_user.id,
                             "Ciao {}, sono DroidModITbot, e gestisco canali e gruppi di DroidModIT!".format(
                                 message.from_user.first_name), reply_markup=markup, disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "Avviami in privato!")


# info command
@bot.message_handler(commands=['info'])
def info(message):
    try:
        if message.from_user.id in admins:
            if message.reply_to_message:
                stato = bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status
                bot.reply_to(message,
                             "*INFO SULL'UTENTE*:\n*NOME:* {}\n*COGNOME:* {}\n*USERNAME:* @{}\n*ID:* {}\n*STATO*: {}".format(
                                 message.reply_to_message.from_user.first_name,
                                 message.reply_to_message.from_user.last_name,
                                 message.reply_to_message.from_user.username,
                                 str(message.reply_to_message.from_user.id), str(stato)), parse_mode="markdown")
            else:
                bot.reply_to(message, str(message.chat.id))
    except Exception as e:
        bot.send_message(me, "errore {}".format(e))


# blah blah blah, read the code
@bot.message_handler(commands=['rmadmin', 'rma', 'unadmin'])
def rmadmin(message):
    try:
        if message.from_user.id == me:
            if message.reply_to_message:
                if message.reply_to_message.from_user.id in admins:
                    admins.remove(message.reply_to_message.from_user.id)
                    bot.send_message(message.chat.id, "{} ({}) non ha più nemmeno il potere di vivere".format(
                        str(message.reply_to_message.from_user.first_name), str(message.reply_to_message.from_user.id)),
                                     parse_mode="html")  # funny xdxd
                elif message.reply_to_message.from_user.id not in admins:
                    bot.send_message(message.chat.id, "Ah ma ancora vive il tipo? È ormai tempo che non respira.",
                                     # funny xdxd
                                     parse_mode="html")
        else:
            bot.send_message(message.chat.id, "HAHAHAHAHAHAAH E SE TI BANNASSI?", parse_mode="html")  # funny xdxd
    except:
        pass


# add mod command
@bot.message_handler(commands=['aggadmin', 'addadmin', 'god'])
def addadmin(message):
    try:
        if message.from_user.id == me:
            if message.reply_to_message:
                admins.append(message.reply_to_message.from_user.id)
                bot.send_message(message.chat.id,
                                 "{} ({}) ora è un minidio, ma attento ad usare i poteri che *******io, *********.".format(
                                     str(message.reply_to_message.from_user.first_name),
                                     str(message.reply_to_message.from_user.id)),
                                 parse_mode="html")  # funny xdxd
            elif message.reply_to_message.from_user.id in admins:
                bot.send_message(message.chat.id, "Il tizio già hai i poteri, cazzo gli vuoi dare più?",
                                 parse_mode="html")  # funny xdxd
        else:
            bot.send_message(message.chat.id, "HAHAHAHAHHAHAHAH ORA TI BANNO *IO JAVA", parse_mode="html")  # funny xdxd
    except:
        pass


@bot.message_handler(commands=['ping'])
def ping(message):
    if message.from_user.id in admins:
        bot.send_message(message.chat.id, 'BONG')  # 11/10 troka


# group posts
@bot.message_handler(commands=['grp', 'group', 'gruppo', 'g'])
def postgruppo(message):
    if message.chat.id in staff:
        grpk = types.InlineKeyboardMarkup()
        mb = types.InlineKeyboardButton(text=('markdown'), callback_data='md')
        hb = types.InlineKeyboardButton(text=('HTML'), callback_data='ht')
        grpk.add(mb)
        grpk.add(hb)
        messaggio = " ".join(message.text.split(" ", 1)[1:])
        global currpostid
        currpostid += 1
        fo = open("{}.txt".format(str(currpostid)), "w")
        fo.write("{}".format(messaggio))
        bot.send_message(message.chat.id, "Scegli la formattazione per il post sul gruppo", reply_markup=grpk)


@bot.callback_query_handler(func=lambda call: True)
def grpcallback(call):
    if call.message:
        if call.data == 'md':
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text="OK, il post sarà inviato con formattazione markdown, invia un messaggio qualsiasi per confermare")
            bot.register_next_step_handler(msg, markdownhandler)
        elif call.data == 'ht':
            msgh = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text="OK, il post sarà inviato con formattazione HTML, invia un messaggio qualsiasi per confermare")
            bot.register_next_step_handler(msgh, htmlhandler)
        elif call.data == 'cmd':
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text="OK, il post sarà inviato con formattazione markdown, invia un messaggio qualsiasi per confermare")
            bot.register_next_step_handler(msg, chmarkdownhandler)
        elif call.data == 'cht':
            msgh = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text="OK, il post sarà inviato con formattazione HTML, invia un messaggio qualsiasi per confermare")
            bot.register_next_step_handler(msgh, chhtmlhandler)


def markdownhandler(message):
    messaggiogrezzo = open('{}.txt'.format(str(currpostid)), 'r')
    messaggio = messaggiogrezzo.read()
    bot.send_message(message.chat.id, "Okay, invio questo testo: {}".format(messaggio))
    try:
        bot.send_message('-1001062309656', messaggio, parse_mode='markdown', disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, 'Si è verificato un errore, eccolo:\n\n\n {}'.format(str(e)))
        return
    bot.send_message(message.chat.id, "Fatto.")


def htmlhandler(message):
    messaggiogrezzo = open('{}.txt'.format(str(currpostid)), 'r')
    messaggio = messaggiogrezzo.read()
    bot.send_message(message.chat.id, "Okay, invio questo testo: {}".format(messaggio))
    try:
        bot.send_message('-1001062309656', messaggio, parse_mode='HTML', disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, 'Si è verificato un errore, eccolo:\n\n\n {}'.format(str(e)))
        return
    bot.send_message(message.chat.id, "Fatto.")


# channel posts
@bot.message_handler(commands=['chan', 'channel', 'canale', 'c'])
def postcanale(message):
    if message.chat.id in staff:
        chank = types.InlineKeyboardMarkup()
        cmb = types.InlineKeyboardButton(text=('MARKDOWN'), callback_data='cmd')
        chb = types.InlineKeyboardButton(text=('html'), callback_data='cht')
        chank.add(cmb)
        chank.add(chb)
        messaggio = " ".join(message.text.split(" ", 1)[1:])
        global currpostidg
        currpostidg += 1
        fo = open("{}.txt".format(str(currpostidg)), "w")
        fo.write("{}".format(messaggio))
        bot.send_message(message.chat.id, "Scegli la formattazione per il post sul canale", reply_markup=chank)


@bot.callback_query_handler(func=lambda call: True)
def chancallback(call):
    if call.message:
        pass  # WHY?????????????????????????????????????????????????


def chmarkdownhandler(message):
    messaggiogrezzo = open('{}.txt'.format(str(currpostidg)), 'r')
    messaggio = messaggiogrezzo.read()
    bot.send_message(message.chat.id, "Okay, invio questo testo sul canale: {}".format(messaggio))
    try:
        bot.send_message(-1001037899324, messaggio, parse_mode='markdown', disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, 'Si è verificato un errore, eccolo:\n\n\n {}'.format(str(e)))
        return
    bot.send_message(message.chat.id, "Fatto.")


def chhtmlhandler(message):
    messaggiogrezzo = open('{}.txt'.format(str(currpostidg)), 'r')
    messaggio = messaggiogrezzo.read()
    bot.send_message(message.chat.id, "Okay, invio questo testo sul canale: {}".format(messaggio))
    try:
        bot.send_message(-1001037899324, messaggio, parse_mode='HTML', disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, 'Si è verificato un errore, eccolo:\n\n\n {}'.format(str(e)))
        return
    bot.send_message(message.chat.id, "Fatto.")


@bot.message_handler(commands=['ab'])
def abilitalimitati(message):
    try:
        if message.from_user.id == me:
            idd = " ".join(message.text.split(" ", 1)[1:])
            if len(idd) > 0:
                allowedusers.append(int(idd))
                bot.send_message(message.chat.id,
                                 "{} è stato abilitato a parlare in @androidmoddingitalia\n lista degli utenti abilitati:{}".format(
                                     idd, str(allowedusers)))
    except:
        pass


# check if user is allowed to send messages with the /t command
@bot.message_handler(commands=['check'])
def check(message):
    if message.chat.type == 'private':
        if message.from_user.id in allowedusers:
            bot.send_message(message.chat.id, "sei abilitato")
        else:
            bot.send_message(message.chat.id, "non sei abilitato")


@bot.message_handler(commands=['t'])
def limitati(message):
    if message.chat.type == 'private':
        if message.from_user.id in allowedusers:
            lol = " ".join(message.text.split(" ", 1)[1:])
            uid = message.from_user.id
            if len(lol) > 0:
                if uid not in flood:
                    bot.send_message('-1001062309656', "{}:\n{}".format(message.from_user.first_name, lol))
                    flood[uid] = 1
                else:
                    flood[uid] += 1
                    if flood[uid] >= 5:
                        bot.send_message(message.chat.id, "stai floodando, aspetta qualche minuto.")
                        time.sleep(60)
                        flood[uid] = 0
                    else:
                        bot.send_message('-1001062309656', "{}:\n{}".format(message.from_user.first_name, lol))
            else:
                bot.send_message(message.chat.id, "messaggio vuoto")
        else:
            bot.send_message(message.chat.id,
                             "non sei autorizzato, chiedi l'autorizzazione nel gruppo ot di @androidmoddingitalia")
    else:
        return


# ban, kick, unban, warn etc.
@bot.message_handler(func=lambda m: True)
def adminccommands(m):
    try:
        if m.reply_to_message:
            if m.text == "#ban" or m.text == "/ban" or m.text == ".ban" or m.text == "!ban":
                if m.from_user.id in admins:
                    if m.reply_to_message:
                        if m.reply_to_message.from_user.id not in admins:
                            bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                            bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                            bot.send_message(m.chat.id,
                                             "{} ({}) è stato bannato da {} ({})".format(
                                                 m.reply_to_message.from_user.first_name,
                                                 m.reply_to_message.from_user.id,
                                                 m.from_user.fist_name, m.from_user.id))
                            bot.send_message('-1001092548412', str(m.reply_to_message.from_user.username) + "(" + str(
                                m.reply_to_message.from_user.id) + ") *è stato bannato da *" + str(
                                m.from_user.username), parse_mode="markdown")
            if m.text == "#kick" or m.text == "/kick" or m.text == ".kick" or m.text == "!kick":
                if m.from_user.id in admins:
                    if m.reply_to_message:
                        if m.reply_to_message.from_user.id not in admins:
                            bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                            bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                            bot.send_message(m.chat.id, "{} ({}) è stato kickato da {} ({})".format(
                                m.reply_to_message.from_user.first_name, m.reply_to_message.from_user.id,
                                m.from_user.fist_name, m.from_user.id))
                            bot.send_message('-1001092548412', str(m.reply_to_message.from_user.username) + "(" + str(
                                m.reply_to_message.from_user.id) + ") *è stato kickato da *" + str(
                                m.from_user.username), parse_mode="markdown")
            if m.text == "#unban" or m.text == ".unban" or m.text == "/unban" or m.text == "!unban":
                if m.from_user.id in admins:
                    if m.reply_to_message:
                        if m.reply_to_message.from_user.id not in admins:
                            bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                            bot.send_message('-1001092548412', str(m.reply_to_message.from_user.username) + "(" + str(
                                m.reply_to_message.from_user.id) + ") *è stato sbannato da *" + str(
                                m.from_user.username),
                                             parse_mode="markdown")
            if m.chat.id in officialchats:
                if m.from_user.id in admins:
                    if m.reply_to_message:
                        if m.text == '#warn':
                            cos = int(m.reply_to_message.from_user.id)
                            c.execute("SELECT * FROM warns WHERE user_id=?", (cos,))
                            if not c.fetchall():
                                c.execute("INSERT INTO warns(user_id, warn) VALUES(?, ?)", (cos, 1))
                                conn.commit()
                                bot.send_message(m.chat.id, "{} ({}) è stato ammonito\n 1/3".format(
                                    m.reply_to_message.from_user.first_name,
                                    str(m.reply_to_message.from_user.id)))
                            else:
                                c.execute("SELECT warn FROM warns WHERE user_id=?", (cos,))
                                tupla = c.fetchone()
                                cosa = list(tupla)
                                total_warns = cosa[0]
                                total_warns += 1
                                if total_warns == 2:
                                    bot.send_message(m.chat.id, "{} ({}) è stato ammonito\n 2/3".format(
                                        m.reply_to_message.from_user.first_name,
                                        str(m.reply_to_message.from_user.id)))
                                    c.execute("UPDATE warns SET warn=? WHERE user_id=?", (2, cos))
                                    conn.commit()
                                if total_warns == 3:
                                    bot.send_message(m.chat.id, "{} ({}) è stato ammonito\n 3/3\n\nBannato.".format(
                                        m.reply_to_message.from_user.first_name,
                                        str(m.reply_to_message.from_user.id)))
                                    bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
                                    c.execute("DELETE FROM warns WHERE userid =?", (cos,))
                                    conn.commit()
                        elif m.text == '#unwarn':
                            cos = int(m.reply_to_message.from_user.id)
                            c.execute("SELECT * FROM warns WHERE user_id=?", (cos,))
                            if not c.fetchall():
                                bot.send_message(m.chat.id, "L'utente non è mai stato ammonito")
                            else:
                                c.execute("SELECT warn FROM warns WHERE user_id=?", (cos,))
                                tuplah = c.fetchone()
                                cosah = list(tuplah)
                                total_warns = cosah[0]
                                total_warns -= 1
                                bot.send_message(m.chat.id, "{} ({}) è stato ammonito\n {}/3".format(
                                    m.reply_to_message.from_user.first_name,
                                    str(m.reply_to_message.from_user.id),
                                    str(total_warns)))
                                c.execute("UPDATE warns SET warn=? WHERE user_id=?", (total_warns, cos))
                                conn.commit()
            if m.text == "#ot":
                if m.from_user.id in admins:
                    if m.reply_to_message:
                        bot.reply_to(m.reply_to_message,
                                     "L'OT in questo gruppo è vietato, sei pregato di entrare nell'apposito gruppo ot.\n[Clicca qui per entrare](https://telegram.me/joinchat/A43QaUD4rP7xT4YA8CFhow)",
                                     parse_mode="markdown")
        else:
            if m.from_user.id in admins:
                try:
                    if m.text.startswith('!ban'):
                        toban = " ".join(m.text.split(" ", 1)[1:])
                        bot.kick_chat_member(m.chat.id, toban)
                    elif m.text.startswith('!unban'):
                        tounban = " ".join(m.text.split(" ", 1)[1:])
                        bot.unban_chat_member(m.chat.id, tounban)
                except:
                    bot.reply_to(m, "si è verificato un errore.")

    except:
        pass


# send nud... ehm rules
@bot.message_handler(commands=['updaterules'])
def updaterulez(message):
    try:
        if message.from_user.id == me:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Gruppo", url="https://telegram.me/androidmoddingitalia"))
            markup.add(types.InlineKeyboardButton("Canale", url="https://telegram.me/moditchan"))
            mex = " ".join(message.text.split(" ", 1)[1:])
            bot.send_message('-1001060734978', str(mex), parse_mode='html', reply_markup=markup,
                             disable_web_page_preview=True)
        else:
            return
    except Exception as e:
        bot.send_message(message.chat.id, "errore: {}".format(str(e)))


# pinned message template
@bot.message_handler(commands=['messaggiofissato'])
def messaggiofissato(message):
    try:
        if message.from_user.id == me:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Gruppo", url="https://telegram.me/androidmoddingitalia"))
            markup.add(types.InlineKeyboardButton("Canale", url="https://telegram.me/moditchan"))
            markup.add(types.InlineKeyboardButton("Regole", url="https://telegram.me/dmitrules"))
            mex = " ".join(message.text.split(" ", 1)[1:])
            bot.send_message('-1001062309656', str(mex), parse_mode='html', reply_markup=markup,
                             disable_web_page_preview=True)
    except Exception as e:
        bot.send_message(message.chat.id, "errore {}".format(str(e)))


# welcome
@bot.message_handler(func=lambda m: True, content_types=['new_chat_member'])
def newmember(message):
    if message.chat.id in officialchats:
        try:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Canale", url="https://telegram.me/moditchan"))
            markup.add(types.InlineKeyboardButton("Regole", url="https://telegram.me/dmitrules"))
            bot.reply_to(message,
                         "Ciao {} benvenuto in DroidModIT, mi raccomando leggi le regole e visita il nostro canale!".format(
                             str(message.new_chat_member.first_name)), parse_mode="markdown", reply_markup=markup)
            bot.send_message('-1001092548412',
                             str(message.new_chat_member.id) + " ( @{}) si è unito al *******io".format(
                                 str(message.new_chat_member.username)))
        except Exception as e:
            bot.send_message('-10010925484412', "@veetaw qua qualcosa non funziona\n\n\n" + str(e))  # WOOOOOOOOOT
    return


bot.polling(none_stop=True)
