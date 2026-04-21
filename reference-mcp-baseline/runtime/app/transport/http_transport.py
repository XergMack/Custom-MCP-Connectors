from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json

class BackendRequestError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class HttpTransport:

    def get_json(self, url, headers):
        req = Request(url, headers=headers)
        try:
            with urlopen(req) as r:
                return json.loads(r.read())
        except HTTPError as e:
            raise BackendRequestError(str(e), e.code)

    def put_bytes(self, url, headers, body):
        req = Request(url, headers=headers, data=body, method="PUT")
        try:
            with urlopen(req) as r:
                return json.loads(r.read())
        except HTTPError as e:
            raise BackendRequestError(str(e), e.code)

    def delete(self, url, headers):
        req = Request(url, headers=headers, method="DELETE")
        try:
            with urlopen(req):
                return None
        except HTTPError as e:
            raise BackendRequestError(str(e), e.code)

    def post_json(self, url, headers, body):
        import json
        req = Request(url, headers=headers, data=json.dumps(body).encode(), method="POST")
        try:
            with urlopen(req) as r:
                return json.loads(r.read())
        except HTTPError as e:
            raise BackendRequestError(str(e), e.code)

    def patch_json(self, url, headers, body):
        import json
        req = Request(url, headers=headers, data=json.dumps(body).encode(), method="PATCH")
        try:
            with urlopen(req) as r:
                return json.loads(r.read())
        except HTTPError as e:
            raise BackendRequestError(str(e), e.code)
