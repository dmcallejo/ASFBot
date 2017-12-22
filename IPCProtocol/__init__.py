import logging
import requests


class IPCProtocolHandler:
    LOG = logging.getLogger('ASFBot.IPCProtocolHandler')

    def __init__(self, host, port, path='/'):
        self.base_url = 'http://' + host + ':' + port + path
        self.LOG.debug("Initialized. Host: %s", self.base_url)

    def get(self, resource, parameters={}):
        if not isinstance(parameters, dict):
            message = "\"parameters\" variable must be a dictionary"
            self.LOG.error(message)
            raise TypeError(message)
        url = self.base_url + resource  # refactor
        self.LOG.debug("Requesting %s with parameters %s", url, str(parameters))
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        self.LOG.debug(response.url)
        self.LOG.debug(response.text)
        return response.text

    def post(self, resource, parameters={}):
        if not isinstance(parameters, dict):
            message = "\"parameters\" variable must be a dictionary"
            self.LOG.error(message)
            raise TypeError(message)
        url = self.base_url + resource  # refactor
        self.LOG.debug("Requesting %s with parameters %s", url, str(parameters))
        response = requests.post(url, params=parameters)
        response.raise_for_status()
        self.LOG.debug(response.url)
        self.LOG.debug(response.text)
        return response.text
