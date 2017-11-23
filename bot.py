#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#import telebot
#from telebot.util import async
from datetime import datetime
import time
import subprocess
import re
import argparse
import logging
import logger

LOG = logging.getLogger('ASFBot')

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbosity", help="Defines log verbosity", choices=['CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'], default='INFO')
parser.add_argument("--port", help="ASF IPC host. Default: 127.0.0.1", default='127.0.0.1')
parser.add_argument("--host", help="ASF IPC port. Default: 1242", default='1242')
parser.add_argument("TELEGRAM_API_TOKEN", type=str, help="Telegram API token given by @botfather.")
parser.add_argument("USER_ALIAS", type=str, help="Telegram alias of the bot owner.")


args = parser.parse_args()

numeric_level = getattr(logging, args.verbosity.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % args.verbosity )
for logger in LOG.handlers:
    logger.setLevel(args.verbosity)

LOG.info("Starting up bot...")

exit()

LOG.debug("ASF IPC host: " + ASF_IPC_HOST)
LOG.debug("ASF IPC port: " + ASF_IPC_PORT)

_last_message=None
_error=False

asf_prepend='/usr/bin/mono /root/ASF/ASF.exe --client '
asf_primary_bot='1'
asf_append=''
cdkey_pattern = re.compile('\w{5}-\w{5}-\w{5}')
_boss=183718
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


@bot.message_handler
def handler(message):
    cid = m.chat.id
    if cid == TELEGRAM_USER_ID:
        if m.text[0] == '/' or "!":
            asf_command=m.text[1:]
            response = execute_command(m,asf_command)
            bot.reply_to(m,"```"+str(response)+"```",parse_mode="Markdown")
        else:
            cdkeys = cdkey_pattern.findall(m.text)
            if len(cdkeys)>0:
                bot.reply_to(m,"Found: "+str(len(cdkeys))+" cdkeys.")
                #auto redeem
                for cdkey in cdkeys:
                    command = "redeem "+asf_primary_bot+" "+cdkey
                    response = execute_command(m,command)
                    bot.send_message(cid,"```"+str(response)+"```",parse_mode="Markdown")

            else:
                log_line=m.text
    else:
        log_line="Not authorised: "+m.text
        log(m,log_line)
        bot.send_message(cid,"https://www.youtube.com/watch?v=glojDYsGAvo")


bot.set_update_listener(listener)

def execute_command(m,command):
    os_command=asf_prepend+command+asf_append
    log(m,"Executing: "+os_command)
    stdout=str(subprocess.check_output(os_command.split(' ',3)))
    slices=stdout.split('WCF response received:',1)
    if(len(slices)>1):
        response=slices[1]
    else:
        response=stdout
    return str(response).strip()

def log(m,text):
    cid = m.chat.id
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    username = get_chat_username(m)
    log_message = ("[%s][%s][%s][%s]" % (now, cid, username, text))
    f = open(log_path + log_file, 'a')
    f.write(log_message + "\n")
    f.close()

def get_chat_username(m):
    cid = m.chat.id
    if cid > 0:
        return m.chat.first_name
    else:
        return m.from_user.first_name


#############################################
# Main loop
#############################################
# Con esto, le decimos al bot que siga funcionando
# incluso si encuentra algún fallo.
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        _error=True
        bot.send_message(_boss,e)
