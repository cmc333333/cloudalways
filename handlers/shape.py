from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import *
from model import *
import logging

class Shape(Handler):
  #override
  def jsonGet(self, element, subelement):
    results = {}
    offset = 0
    query = ShapeField.all().order('shape')
    count = query.count()
    while offset < count:
      for field in query.fetch(20, offset):
        offset = offset + 1
        if not field.shape in results:
          results[field.shape] = {}
        results[field.shape][field.name] = {'type': field.fieldType, 'required': field.required}
    self.success(results)

class ShapeElement(Handler):
  #override
  def jsonGet(self, shape, subelement):
    query = ShapeField.all().filter('shape =', shape)
    results = {}
    for field in query.fetch(50): # Each shape may have at most 50 fields
      results[field.name] = {'type': field.fieldType, 'required': field.required}
    if len(results) == 0:
      self.error(404)
    else:
      self.success(results)
  #override
  def jsonDelete(self, shape, subelement):
    query = ShapeField.all().filter('shape = ', shape)
    if query.count() == 0:
      self.error(404)
    else:
      for field in query.fetch(50):
        field.delete()
      self.success()
  #override
  def jsonPut(self, body, shape, subelement):
    fields = body.keys()
    if len(fields) == 0:
      self.fail('must have at least one field')
    elif len(fields) > 50:
      self.fail('each shape may have at most 50 fields')
    else:
      # verify that every field has a type and that said type is valid
      valid = True
      for field in fields:
        if not isinstance(body[field], dict) or 'type' not in body[field]:
          valid = False
          self.fail(field + ' does not have a type')
          break
        if body[field]['type'] not in ShapeFieldTypes:
          valid = False
          self.fail(str(body[field]['type']) + ' is an invalid type')
          break

      if valid:
        existing = ShapeField.all().filter('shape =', shape).fetch(50)
        new = body.keys()
        for field in existing:
          if field.name in fields: # Modifying
            new.remove(field.name)
            field.updateType(body[field.name]['type']).put()
          else:
            field.delete()
        # Create the new ones
        for field in new:
          ShapeField(shape=shape, name=field, fieldType=body[field]['type']).put()

        self.success()

class ShapeSubelement(Handler):
  #override
  def jsonGet(self, shape, field):
    query = ShapeField.all().filter('shape =', shape).filter('name =', field)
    if query.count() == 0:
      self.error(404)
    else:
      field = query.fetch(1)[0]
      result = {'type': field.fieldType, 'required': field.required}
      self.success(result)
  #override
  def jsonDelete(self, shape, field):
    query = ShapeField.all().filter('shape = ', shape).filter('name =', field)
    if query.count() == 0:
      self.error(404)
    else:
      query.fetch(1)[0].delete()
      self.success()
  #override
  def jsonPut(self, body, shape, field):
    if 'type' not in body:
      valid = False
      self.fail(field + ' does not have a type')
    elif body['type'] not in ShapeFieldTypes:
      valid = False
      self.fail(str(body['type']) + ' is an invalid type')
    else:
      existing = ShapeField.all().filter('shape =', shape).filter('name =', field).fetch(1)
      if len(existing) > 0:
        existing[0].updateType(body['type']).put()
      else:
        ShapeField(shape=shape, name=field, fieldType=body['type']).put()
      self.success()

application = webapp.WSGIApplication([
  ('/shape', Shape),
  (r'/shape/(.*)/(.*)', ShapeSubelement),
  (r'/shape/(.*)', ShapeElement)
  ], debug=True)

def main():
  run_wsgi_app(application)
if __name__ == "__main__":
  main()
