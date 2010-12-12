from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import *
from model import *
import logging

class Form(Handler):
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
    for field in query.fetch(50): # Each form may have at most 50 fields
      results[field.name] = {'type': field.fieldType, 'required': field.required}
    if len(results) == 0:
      self.error(404)
    else:
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
  def jsonPut(self, body, form, subelement):
    fields = body.keys()
    if len(fields) == 0:
      self.fail('must have at least one field')
    elif len(fields) > 50:
      self.fail('each form may have at most 50 fields')
    else:
      # verify that every field has a type and that said type is valid
      valid = True
      for field in fields:
        if not isinstance(body[field], dict) or 'type' not in body[field]:
          valid = False
          self.fail(field + ' does not have a type')
          break
        if body[field]['type'] not in FormFieldTypes:
          valid = False
          self.fail(body[field]['type'] + ' is an invalid type')
          break

      if valid:
        existing = FormField.all().filter('form =', form).fetch(50)
        new = body.keys()
        for field in existing:
          if field.name in fields: # Modifying
            new.remove(field.name)
            field.updateType(body[field.name]['type']).put()
          else:
            field.delete()
        # Create the new ones
        for field in new:
          FormField(form=form, name=field, fieldType=body[field]['type']).put()

        self.success()

application = webapp.WSGIApplication([
  ('/form', Form),
  (r'/form/(.*)', FormElement)
  ], debug=True)

def main():
  run_wsgi_app(application)
if __name__ == "__main__":
  main()
