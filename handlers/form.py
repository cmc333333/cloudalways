from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import *
from model import *

class Form(Handler):
  #override
  def jsonPost(self, body, element, subelement):
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
        self.success({"name": body['name']})
      except FormFieldException as e:
        self.fail(e.value)
  #override
  def jsonGet(self, element, subelement):
    results = {}
    offset = 0
    query = FormField.all().order('form')
    count = query.count()
    while offset < count:
      for field in query.fetch(20, offset):
        offset = offset + 1
        if not field.form in results:
          results[field.form] = {}
        results[field.form][field.name] = {'type': field.fieldType, 'required': field.required}
    self.success(results)

class FormElement(Handler):
  #override
  def jsonGet(self, element, subelement):
    query = FormField.all().filter('form =', element)
    results = {}
    offset = 0
    count = query.count()
    while offset < count:
      for field in query.fetch(20, offset):
        offset = offset + 1
        results[field.name] = {'type': field.fieldType, 'required': field.required}
    self.success(results)
  #override
  def jsonDelete(self, element, subelement):
    query = FormField.all().filter('form = ', element)
    if query.count() == 0:
      self.fail("no such forms")
    else:
      for field in query.fetch(50):
        field.delete()
      self.success()
  #override
  def jsonPut(self, body, element, subelement):
    if not 'fields' in body:
      self.fail('"fields" must be in the json body')
    elif not isinstance(body['fields'], dict):
      self.fail('"fields" must be an object')
    elif len(body['fields']) == 0:
      self.fail('"fields" must have length > 0')
    elif len(body['fields']) > 50:
      self.fail('each form may have at most 50 fields')
    else:
      try:
        existing = FormField.all().filter('form =', element).fetch(100)  # <= 50 in the db <= 50 new
        new = body['fields'].keys()
        toDelete = []
        toSave = []
        for field in existing:
          if field.name in body['fields']: # Modifying
            new.remove(field.name)
            field.fromDict(field.form, body['fields'][field.name], True)
            toSave.append(field)
          else:
            toDelete.append(field)
        # Create the new ones
        for field in new:
          toSave.append(FormField().fromDict(body['name'], field))

        for field in toSave:
          field.put()
        for field in toDelete:
          field.deleteAndUpdate()
      except FormFieldException as e:
        self.fail(e.value)

application = webapp.WSGIApplication([
  ('/form', Form),
  (r'/form/(.*)', FormElement)
  ], debug=True)

def main():
  run_wsgi_app(application)
if __name__ == "__main__":
  main()
