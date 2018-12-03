import logging
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def set_logger(name):
    global logger
    # create logger with 'spam_application'
    logger = logging.getLogger(name)
    logger.setLevel(DEFAULT_LOG_LEVEL)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(DEFAULT_LOG_LEVEL)
    # create formatter and add it to the handlers
    ch.setFormatter(DEFAULT_FORMATTER)
    # add the handlers to the logger
    logger.addHandler(ch)
    return logger


def set_level(verbosity):
    numeric_level = get_numeric_log_level(verbosity)
    for c_logger in logger.handlers:
        c_logger.setLevel(numeric_level)


def get_numeric_log_level(verbosity):
    numeric_level = getattr(logging, verbosity.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % verbosity)
    return numeric_level


def get_logger(name=None):
    if name:
        return logger.getChild(name)
    return logger


def add_file_handler(file_path, log_level=DEFAULT_LOG_LEVEL, formatter=DEFAULT_FORMATTER):
    fh = logging.FileHandler(file_path)
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)