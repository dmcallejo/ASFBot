import re

import logger
import requests

LOG = None


class IPCProtocolHandler:

    AUTH_HEADER = 'Authentication'

    headers = {'user-agent': 'ASFBot',
               'Accept': 'application/json'}

    def __init__(self, host, port, path='/', password=None):
        global LOG
        LOG = logger.get_logger(__name__)
        self.base_url = 'http://' + host + ':' + port + path
        if password:
            self.headers[self.AUTH_HEADER] = password
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        LOG.debug("Initialized. Host: %s", self.base_url)

    def get(self, resource, parameters=None):
        if parameters is None:
            parameters = {}
        if not isinstance(parameters, dict):
            message = "\"parameters\" variable must be a dictionary"
            LOG.error(message)
            raise TypeError(message)
        url = self.base_url + resource  # TODO: refactor
        LOG.debug("Requesting %s with parameters %s", url, str(parameters))
        try:
            response = self.session.get(url, params=parameters)
            response.raise_for_status()
            LOG.debug(response.url)
            LOG.debug(response.json())
            return response.json()
        except requests.exceptions.RequestException as ex:
            LOG.error("Error Requesting %s with parameters %s", url, str(parameters))
            LOG.exception(ex)
            reason = extract_reason_from_exception(ex)
            return {
                'Success': False,
                'Message': reason
            }

    def post(self, resource, payload=None):
        if payload:
            if not isinstance(payload, dict):
                message = "\"payload\" must be a dictionary"
                LOG.error(message)
                raise TypeError(message)
        url = self.base_url + resource  # TODO: refactor
        LOG.debug("Requesting %s with payload %s", url, str(payload))
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        LOG.debug(response.url)
        LOG.debug(response.json())
        return response.json()


def extract_reason_from_exception(ex: Exception):
    if len(ex.args) > 0:
        ex_args = ex.args[0]
        if isinstance(ex_args, Exception):
            ex_reason = ex_args.reason
            return extract_reason_from_exception(ex_reason)
        else:
            return re.match('(^.*0x\\w+>:\\s+)?(?P<reason>.*)$', ex_args).group('reason')

