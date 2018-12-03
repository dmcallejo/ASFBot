#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import telebot
import re
import argparse
import logger
import logging
from ASFConnector import ASFConnector


_REGEX_CDKEY = re.compile('\w{5}-\w{5}-\w{5}')
_REGEX_COMMAND_BOT_ARGS = '^[/!]\w+\s*(?P<bot>\w+)?\s+(?P<arg>.*)'
_REGEX_COMMAND_RAW = '^[/!](?P<input>(?P<command>\w+).*)'
_REGEX_COMMAND = '^[/!]\w+\s*(?P<bot>\w+)?'
_ENV_TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
_ENV_TELEGRAM_USER_ALIAS = "TELEGRAM_USER_ALIAS"
_ENV_ASF_IPC_HOST = "ASF_IPC_HOST"
_ENV_ASF_IPC_PORT = "ASF_IPC_PORT"
_ENV_ASF_IPC_PASSWORD = "ASF_IPC_PASSWORD"

LOG = logger.set_logger('ASFBot')

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

logger.set_level(args.verbosity)

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
    asf_info = asf_connector.get_asf_info()
    LOG.info('ASF Instance replied: {}'.format(asf_info['Message']))
    if not asf_info['Success']:
        LOG.warning('ASF Instance message was unsuccesful. %s', str(asf_info))

except Exception as e:
    LOG.critical("Couldn't communicate with ASF. Host: '%s' Port: '%s' \n %s",
                 args.host, args.port, str(e))
    exit(1)

bot = telebot.TeleBot(args.token)


def is_user_message(message):
    """ Returns if a message is from the owner of the bot comparing it to the user alias provided on startup. """
    username = message.chat.username
    return username == args.alias


@bot.message_handler(func=is_user_message, commands=['status'])
def redeem_command(message):
    LOG.debug("Received status message: %s", str(message))
    match = re.search(_REGEX_COMMAND, message.text)
    if not match:
        bot.reply_to(message, "Invalid command. Usage:\n`/status <bot>`", parse_mode="Markdown")
        return
    bot_arg = match.group('bot') if match.group('bot') else 'ASF'
    response = asf_connector.get_bot_info(bot_arg)
    LOG.debug("Response to redeem message: %s", str(response))
    bot.reply_to(message, "```\n" + str(response) + "\n```", parse_mode="Markdown")


@bot.message_handler(commands=['redeem'])
def redeem_command(message):
    LOG.debug("Received redeem message: %s", str(message))
    match = re.search(_REGEX_COMMAND_BOT_ARGS, message.text)
    if not match:
        bot.reply_to(message, "Missing arguments. Usage:\n`/redeem <bot> <keys>`", parse_mode="Markdown")
        return
    bots = match.group('bot') if match.group('bot') else 'ASF'
    keys = match.group('arg')
    response = asf_connector.bot_redeem(bots, keys)
    LOG.debug("Response to redeem message: %s", str(response))
    bot.reply_to(message, "```\n" + str(response) + "\n```", parse_mode="Markdown")


@bot.message_handler(func=is_user_message, regexp=_REGEX_COMMAND_RAW)
def command_handler(message):
    """
    Handler only for unsupported commands.
    """
    LOG.debug("Received command: %s", str(message))
    match = re.search(_REGEX_COMMAND_RAW, message.text)
    if not match:
        bot.reply_to(message, "Invalid command.", parse_mode="Markdown")
        return
    command = match.group('input')
    response = asf_connector.send_command(command)
    bot.reply_to(message, response, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def check_for_cdkeys(message):
    """
    Sync handler for the rest of the messages. It searchs for cdkeys and redeems them.
    """
    cdkeys = set(_REGEX_CDKEY.findall(message.text))
    if len(cdkeys) > 0:
        response = asf_connector.bot_redeem('ASF', cdkeys)
        bot.reply_to(message, "```\n" + str(response) + "\n```", parse_mode="Markdown")
    else:
        LOG.debug("Bypassed message: %s \n from user alias %s.",
                  message.text, message.chat.username)


try:
    LOG.debug("Polling started")
    bot.polling(none_stop=True)
except Exception as e:
    LOG.critical(str(e))
    LOG.exception(e)
