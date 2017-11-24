#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

import telebot
from telebot.util import async
from datetime import datetime
import time
import subprocess
import re
import argparse
import logging
import logger
from ASFConnector import ASFConnector

LOG = logging.getLogger('ASFBot')

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbosity", help="Defines log verbosity",
                    choices=['CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'], default='INFO')
parser.add_argument("--host", help="ASF IPC host. Default: 127.0.0.1", default='127.0.0.1')
parser.add_argument("--port", help="ASF IPC port. Default: 1242", default='1242')
parser.add_argument("TELEGRAM_API_TOKEN", type=str, help="Telegram API token given by @botfather.")
parser.add_argument("USER_ALIAS", type=str, help="Telegram alias of the bot owner.")


args = parser.parse_args()

numeric_level = getattr(logging, args.verbosity.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % args.verbosity)
for logger in LOG.handlers:
    logger.setLevel(numeric_level)

LOG.info("Starting up bot...")
LOG.debug("ASF IPC host: " + args.host)
LOG.debug("ASF IPC port: " + args.port)
asf_connector = ASFConnector(args.host, args.port)
asf_connector.send_command("status")

_cdkey_pattern = re.compile('\w{5}-\w{5}-\w{5}')

LOG.debug("Telegram token: " + args.TELEGRAM_API_TOKEN)
LOG.debug("User alias: " + args.USER_ALIAS)

bot = telebot.TeleBot(args.TELEGRAM_API_TOKEN)


#@bot.message_handler
def handler(messages):
    for message in messages:
        fine_handler(message)


def fine_handler(message):
    LOG.debug("Received message: " + str(message))
    cid = message.chat.id
    username = message.chat.username
    if username == args.USER_ALIAS:
        first_char = message.text[0]
        if first_char == '/' or first_char == '!':
            user_input = message.text[1:]
            slices = user_input.split(' ', 3)
            asf_command = slices[0]
            if len(slices) > 2:
                target_bot = slices[1]
                arguments = slices[2]
                response = asf_connector.send_command(
                    asf_command, bot=target_bot, arguments=arguments)
            elif len(slices) > 1:
                arguments = slices[1]
                response = asf_connector.send_command(asf_command, arguments=arguments)
            else:
                response = asf_connector.send_command(asf_command)

            bot.reply_to(message, "```" + str(response) + "```", parse_mode="Markdown")
        else:
            cdkeys = _cdkey_pattern.findall(message.text)
            if len(cdkeys) > 0:
                bot.reply_to(message, "Found: " + str(len(cdkeys)) + " cdkeys.")
                # auto redeem
                for cdkey in cdkeys:
                    command = "redeem"
                    response = asf_connector.send_command(command, arguments=cdkey)
                    bot.send_message(cid, "```" + str(response) + "```", parse_mode="Markdown")

            else:
                LOG.debug(message.text)
    else:
        LOG.debug("Not authorised: " + message.text)
        bot.send_message(cid, "https://www.youtube.com/watch?v=glojDYsGAvo")


bot.set_update_listener(handler)


try:
    LOG.debug("Polling started")
    bot.polling(none_stop=True)
except Exception as e:
    LOG.error(str(e))
    raise e
