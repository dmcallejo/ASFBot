import logging
import requests
from IPCProtocol import IPCProtocolHandler


class ASFConnector:
    LOG = logging.getLogger('ASFBot.' + __name__)

    def __init__(self, host='127.0.0.1', port='1242', path='/IPC'):
        self.host = host
        self.port = port
        self.path = path

        self.LOG.debug(__name__ + " initialized. Host: '%s'. Port: '%s'", host, port)
        self.connection_handler = IPCProtocolHandler(host, port, path)

    def send_command(self, command, arguments='', bot='ASF'):
        parameters = {"command": str(command) + ' ' + str(bot) + ' ' + str(arguments)}
        try:
            response = self.connection_handler.get('', parameters)
        except requests.exceptions.ConnectionError as connection_error:
            self.LOG.error("Error sending command %s: %s",
                           parameters["command"], str(connection_error))
            raise connection_error
        # TODO: Output parse?

        return response
