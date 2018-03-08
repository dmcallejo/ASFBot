import logging
import requests
import json
from IPCProtocol import IPCProtocolHandler


class ASFConnector:
    LOG = logging.getLogger('ASFBot.' + __name__)

    def __init__(self, host='127.0.0.1', port='1242', path='/Api'):
        self.host = host
        self.port = port
        self.path = path

        self.LOG.debug(__name__ + " initialized. Host: '%s'. Port: '%s'", host, port)
        self.connection_handler = IPCProtocolHandler(host, port, path)

    def send_command(self, command, arguments='', bot='ASF'):
        self.LOG.debug("Send command: " + command + ", bot: " + bot + ", arguments: " + arguments)
        asf_command_resource = '/Command'
        user_command_resource = '/' + "+".join(str(command).split())
        user_arguments_resource = '+' + bot + ' ' + "+".join(str(arguments).split())
        resource = asf_command_resource + user_command_resource + user_arguments_resource.strip()
        try:
            response = self.connection_handler.post(resource)
        except requests.exceptions.ConnectionError as connection_error:
            self.LOG.error("Error sending command %s: %s",
                           command, str(connection_error))
            raise connection_error
        json_response = json.loads(response)
        return json_response["Result"]
