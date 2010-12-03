from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import *
from model import FormField

class Form(Handler):
  #override
  def jsonPost(self, body):
    if not 'name' in body:
      self.fail('"name" must be in the json body')
    elif not isinstance(body['name'], unicode):
      self.fail('"name" must be a string')
    elif not 'fields' in body:
      self.fail('"fields" must be in the json body')
    elif not isinstance(body['fields'], list):
      self.fail('"fields" must be an array')
    elif len(body['fields']) == 0:
      self.fail('"fields" must have length > 0')
    elif FormField.all().filter('form =', body['name']).count() > 0:
      self.fail('Form with the name ' + body['name'] + ' already exists')
    else:
      try:
        fields = []
        for field in body['fields']:
          fields.append(FormField().fromDict(body['name'], field))
        for field in fields:
          field.put()
      except FormFieldException as e:
        self.fail(e.value)
        
application = webapp.WSGIApplication([('/', Form)], debug=True)

def main():
  run_wsgi_app(application)
if __name__ == "__main__":
  main()
