import httplib2
import json

class Server(object):
  def __init__(self):
    self.baseUrl = "http://localhost:8080/"
    self.http = httplib2.Http(".cache")
  def get(self, path):
    return self._process(self.baseUrl + path, "GET", None, None)
  def delete(self, path):
    return self._process(self.baseUrl + path, "DELETE", None, None)
  def post(self, path, body = None, headers = None):
    if not headers:
      headers = {}
    if body:
      headers['content-type'] = 'application/json'
      body = json.dumps(body)
    return self._process(self.baseUrl + path, "POST", body, headers)
  def put(self, path, body = None, headers = None):
    if not headers:
      headers = {}
    if body:
      headers['content-type'] = 'application/json'
      body = json.dumps(body)
    return self._process(self.baseUrl + path, "PUT", body, headers)
  def _process(self, url, method, body, headers):
    if not headers:
      headers = {}
    if body:
      resp, content = self.http.request(url, method, body=body, headers=headers)
    else:
      headers['Content-length'] = "0"
      resp, content = self.http.request(url, method, headers=headers)
    if resp['status'] != '200':
      return (False, {"body": body})
    else:
      j = json.loads(content)
      if j['status'] != 'success':
        return (False, j)
      else:
        return (True, j)

