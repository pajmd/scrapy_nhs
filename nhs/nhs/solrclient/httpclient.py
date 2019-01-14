import requests


class HttpClientException(Exception):
    pass


class HttpClient(object):
    def __init__(self, host, port=None, timeout=5):
        self.port = port
        self.host = 'http://%s:%s' % (host, port) if port else 'http://%s' % host
        self.timeout = timeout
        self.header = {'user-agent': 'nhs/0.0.1'}

    def get(self, url, json_payload):
        r = requests.get(self.full_url(url), headers=self.header, params=json_payload)
        try:
            r.raise_for_status()
            return r
        except requests.HTTPError:
            return r

    def post(self, url, json_payload=None, header=None, files=None):
        """
        Post either a json payload or files
        :param url:
        :param json_payload:
        :param header:
        :param files: single file as a string or a list of files. It is best to pass the full path of a  each file.
        :return: an requests.Response() or list of requests.Response()
        """
        headers = self.header.copy()
        if header:
            headers.update(header)

        if (json_payload and files) or (json_payload is None and files is None):
            raise HttpClientException("Error POST - can't post both json_payload and files")
        if files:
            if isinstance(files, list):
                with requests.session() as s:
                    responses = []
                    for file in files:
                        with open(file, 'rb') as f:
                            r = s.post(self.full_url(url), data=f, headers=headers)
                        try:
                            r.raise_for_status()
                            responses.append(r)
                        except requests.HTTPError:
                            responses.append(r)
                return responses
            else:
                with open(files, 'rb') as f:
                    r = requests.post(self.full_url(url), data=f, headers=headers)
        else:
            r = requests.post(self.full_url(url), headers=headers, json=json_payload)
        try:
            r.raise_for_status()
            return r
        except requests.HTTPError:
            return r

    def full_url(self, url):
        return '%s/%s' % (self.host, url)
