from google.appengine.ext import webapp
import json

class Handler(webapp.RequestHandler):
  def post(self, element=None, subelement=None):
    if not self.__jsonReq():
      self.fail("Must have content-type: application/json")
    else:
      try:
        body = json.loads(self.request.body)
        self.jsonPost(body, element, subelement)
      except ValueError:
        self.fail("Invalid JSON")
  def jsonPost(self, body, element, subelement):
    self.error(405)
  def get(self, element=None, subelement=None):
    self.jsonGet(element, subelement)
  def jsonGet(self, element, subelement):
    self.error(405)
  def delete(self, element=None, subelement=None):
    self.jsonDelete(element, subelement)
  def jsonDelete(self, element, subelement):
    self.error(405)
  def put(self, element=None, subelement=None):
    if not self.__jsonReq():
      self.fail("Must have content-type: application/json")
    else:
      try:
        body = json.loads(self.request.body)
        self.jsonPut(body, element, subelement)
      except ValueError:
        self.fail("Invalid JSON")
  def jsonPut(self, body, element, subelement):
    self.error(405)
  def __jsonReq(self):
    for (key, value) in self.request.headers.items():
      if key.lower() == "content-type" and value.lower() == "application/json":
        return True
    return False
  def fail(self, message):
    self.response.set_status(400)
    self.response.headers['Content-Type'] = 'application/json'
    response = {"status": "failure", "failure_reason": message}
    self.response.out.write(json.dumps(response))
  def success(self, response = {}):
    self.response.headers['Content-Type'] = 'application/json'
    response['status'] = 'success'
    self.response.out.write(json.dumps(response))
