import logger
import requests

LOG = None


class IPCProtocolHandler:

    AUTH_HEADER = 'Authentication'

    headers = {'user-agent': 'ASFBot'}

    def __init__(self, host, port, path='/', password=None):
        global LOG
        LOG = logger.get_logger(__name__)
        self.base_url = 'http://' + host + ':' + port + path
        if password:
            self.headers[self.AUTH_HEADER] = password
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        LOG.debug("Initialized. Host: %s", self.base_url)

    def get(self, resource, parameters={}):
        if not isinstance(parameters, dict):
            message = "\"parameters\" variable must be a dictionary"
            LOG.error(message)
            raise TypeError(message)
        url = self.base_url + resource  # TODO: refactor
        LOG.debug("Requesting %s with parameters %s", url, str(parameters))
        response = self.session.get(url, params=parameters)
        LOG.debug(response.url)
        LOG.debug(response.json())
        return response.json()

    def post(self, resource, payload=None):
        if payload:
            if not isinstance(payload, dict):
                message = "\"payload\" must be a dictionary"
                LOG.error(message)
                raise TypeError(message)
        url = self.base_url + resource  # TODO: refactor
        LOG.debug("Requesting %s with payload %s", url, str(payload))
        response = self.session.post(url, json=payload)
        LOG.debug(response.url)
        LOG.debug(response.json())
        return response.json()
