import logging
from IPCProtocol import IPCProtocolHandler


class ASFConnector:
    LOG = logging.getLogger('ASFBot.' + __name__)

    def __init__(self, host='127.0.0.1', port='1242', path='/IPC'):
        self.host = host
        self.port = port
        self.path = path

        self.LOG.debug(__name__ + " initialized. Host: " + host +
                       ". Port: " + port + ". Path: " + str(path))
        self.connection_handler = IPCProtocolHandler(host, port, path)
