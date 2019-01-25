from solrclient.httpclient import HttpClientException, HttpClient
import pytest
import requests
from unittest.mock import patch, MagicMock


@patch("builtins.open")
@pytest.mark.parametrize("jsonpayload, files, header, expected",
                         [
                             ({'payload': 'stuff'}, None, None, 'SomeResponse'),
                             ({'payload': 'stuff'}, None, {'WHAT': 'header val'}, 'SomeResponse'),
                             (None, 'a_file', None, 'SomeResponse'),
                             (None, ['file1', 'file2'], None, 'SomeResponse'), # return the last response error or not
                             pytest.param(None, None, None, 'HttpClientException',
                                          marks=pytest.mark.xfail(raises=HttpClientException)),
                             pytest.param({'payload': 'stuff'}, 'a_file', None, 'HttpClientException',
                                          marks=pytest.mark.xfail(raises=HttpClientException)),
                         ]
                         )
def test_post(mock_open, monkeypatch, jsonpayload, files, header, expected):
    class SomeResponse(object):
        def raise_for_status(self):
            pass

        def __repr__(self):
            return 'SomeResponse'

        def __str__(self):
            return 'SomeResponse'

    def mock_post(p1, headers, json=None, data=None):
        return SomeResponse()

    def mock_session_post(self, p1, headers, json=None, data=None):
        return SomeResponse()

    mock_open.return_value = MagicMock()

    monkeypatch.setattr(requests, 'post', mock_post)
    monkeypatch.setattr(requests.Session, 'post', mock_session_post)

    httpclient = HttpClient('some_host', 1234)
    r = httpclient.post("some/url", json_payload=jsonpayload, header=header, files=files)
    # if header:
    #     # key, values in common
    #     rd = header.items() & expected_header.items()
    #     assert len(rd) == len(header)
    if isinstance(r, list):
        for i, ri in enumerate(r):
            assert str(ri) == expected[i]
    else:
        assert str(r) == expected


@pytest.mark.parametrize("p1, p2, p3, expected", [
    ({'json': 'object'}, [1, 'list'], 'string', False),
    (None, [1, 'list'], None, True),
    (None, None, None, False),
    (None, None, 2, True),
])
def test_is_one_olny_set(p1, p2, p3, expected):
    rc = HttpClient.is_one_olny_set(p1, p2, p3)
    assert expected == rc
