import logging


class IPCProtocolHandler:
    LOG = logging.getLogger('ASFBot.IPCProtocolHandler')

    def __init__(self, host, port, path='/'):
        self.host = host
        self.port = port
        self.path = path

        self.LOG.debug("Initialized. Host: " + host +
                       ". Port: " + port + ". Path: " + path)
        self.connection_handler = IPCConnectionHandler(host, port, path)


class IPCConnectionHandler:
    LOG = logging.getLogger('ASFBot.IPCConnectionHandler')

    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path

        self.LOG.debug("Initialized. Host: " + host +
                       ". Port: " + port + ". Path: " + path)
