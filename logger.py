import logging
DEFAULT_LOG_LEVEL = logging.DEBUG

# create logger with 'spam_application'
logger = logging.getLogger('ASFBot')
logger.setLevel(DEFAULT_LOG_LEVEL)
# create file handler which logs even debug messages
fh = logging.FileHandler('ASFBot.log')
fh.setLevel(DEFAULT_LOG_LEVEL)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(DEFAULT_LOG_LEVEL)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.debug("Logger initialized")
