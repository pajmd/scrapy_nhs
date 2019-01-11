import requests


class HttpClient(object):
    def __init__(self, host, port=None, timeout=5):
        self.port = port
        self.host = 'http://%s:%s' % (host, port) if port else 'http://%s' % host
        self.timeout = timeout
        self.header = {'user-agent': 'nhs/0.0.1'}

    def get(self, url, json_payload):
        r = requests.get(self.full_url(url), headers=self.headers, params=json_payload)
        r.raise_for_status()
        return r

    def post(self, url, json_payload):
        r = requests.post(self.full_url(url), headers=self.headers, json=json_payload)
        r.raise_for_status()
        return r

    def full_url(self, url):
        return '%s/%s' % (self.host, url)
