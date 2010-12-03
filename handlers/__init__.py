from google.appengine.ext import webapp
import json

class Handler(webapp.RequestHandler):
  def post(self):
    if not self.__jsonReq():
      self.fail("Must have content-type: application/json")
    else:
      try:
        body = json.loads(self.request.body)
        self.jsonPost(body)
      except ValueError:
        self.fail("Invalid JSON")
  def jsonPost(self, body):
    self.error(405)
  def __jsonReq(self):
    for (key, value) in self.request.headers.items():
      if key.lower() == "content-type" and value.lower() == "application/json":
        return True
    return False
  def fail(self, message):
    self.response.set_status(400)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(message)
