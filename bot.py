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

_REGEX_CDKEY = re.compile('\w{5}-\w{5}-\w{5}')
_REGEX_COMMAND = '^[!/].*$'
_ENV_TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
_ENV_TELEGRAM_USER_ALIAS = "TELEGRAM_USER_ALIAS"
_ENV_ASF_IPC_HOST = "ASF_IPC_HOST"
_ENV_ASF_IPC_PORT = "ASF_IPC_PORT"
_ENV_ASF_IPC_PASSWORD = "ASF_IPC_PASSWORD"

LOG = logging.getLogger('ASFBot')

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbosity", help="Defines log verbosity",
                    choices=['CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'], default='INFO')
parser.add_argument("--host", help="ASF IPC host. Default: 127.0.0.1", default='127.0.0.1')
parser.add_argument("--port", help="ASF IPC port. Default: 1242", default='1242')
parser.add_argument("--password", help="ASF IPC password.", default=None)
parser.add_argument("--token", type=str,
                    help="Telegram API token given by @botfather.", default=None)
parser.add_argument("--alias", type=str, help="Telegram alias of the bot owner.", default=None)
args = parser.parse_args()

numeric_level = getattr(logging, args.verbosity.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % args.verbosity)
for logger in LOG.handlers:
    logger.setLevel(numeric_level)

# Telegram related environment variables.
try:
    args.token = os.environ[_ENV_TELEGRAM_BOT_TOKEN]
except KeyError as key_error:
    if not args.token:
        LOG.critical(
            "No telegram bot token provided. Please do so using --token argument or %s environment variable.", _ENV_TELEGRAM_BOT_TOKEN)
        exit(1)

try:
    args.alias = os.environ[_ENV_TELEGRAM_USER_ALIAS]
except KeyError as key_error:
    if not args.alias:
        LOG.critical(
            "No telegram user alias provided. Please do so using --alias argument or %s environment variable.", _ENV_TELEGRAM_USER_ALIAS)
        exit(1)

# ASF IPC related environment variables.
try:
    args.host = os.environ[_ENV_ASF_IPC_HOST]
except KeyError as key_error:
    pass
try:
    args.port = os.environ[_ENV_ASF_IPC_PORT]
except KeyError as key_error:
    pass
try:
    args.password = os.environ[_ENV_ASF_IPC_PASSWORD]
except KeyError as key_error:
    if not args.password:
        LOG.debug("No IPC Password provided.")
    pass
if args.alias[0] == '@':
    args.alias = args.alias[1:]

LOG.info("Starting up bot...")
LOG.debug("Telegram token: %s", args.token)
LOG.debug("User alias: %s", args.alias)
LOG.debug("ASF IPC host: %s", args.host)
LOG.debug("ASF IPC port: %s", args.port)

asf_connector = ASFConnector(args.host, args.port, password=args.password)

try:
    asf_connector.send_command("status")
except Exception as e:
    LOG.critical("Couldn't communicate with ASF. Host: '%s' Port: '%s' \n %s",
                 args.host, args.port, str(e))
    exit(1)

bot = telebot.TeleBot(args.token)


def is_user_message(message):
    """ Returns if a message is from the owner of the bot comparing it to the user alias provided on startup. """
    username = message.chat.username
    return username == args.alias


@async()
@bot.message_handler(func=is_user_message, regexp=_REGEX_COMMAND)
def command_handler(message):
    """
    Async handler only for user commands.
    """
    LOG.debug("Received message: %s", str(message))
    cid = message.chat.id
    user_input = message.text[1:]
    slices = user_input.split(' ', 3)
    asf_command = slices[0]
    # this is a mess
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


@bot.message_handler(content_types=['text'])
def check_for_cdkeys(message):
    """
    Sync handler for the rest of the messages. It searchs for cdkeys and redeems them.
    """
    cdkeys = set(_REGEX_CDKEY.findall(message.text))
    cid = message.chat.id
    if len(cdkeys) > 0:
        bot.reply_to(message, "Found: " + str(len(cdkeys)) + " cdkeys.")
        # auto redeem
        for cdkey in cdkeys:
            command = "redeem"
            response = asf_connector.send_command(command, arguments=cdkey)
            bot.send_message(cid, "```" + str(response) + "```", parse_mode="Markdown")
    else:
        LOG.debug("Bypassed message: %s \n from user alias %s.",
                  message.text, message.chat.username)


try:
    LOG.debug("Polling started")
    bot.polling(none_stop=True)
except Exception as e:
    LOG.critical(str(e))
    LOG.exception(e)
