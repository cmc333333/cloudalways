from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import *
from model import *
import logging

class Data(Handler):
  #override
  def jsonGet(self, _, _1):
    dataQuery = Datum.all().order('shape')
    data = []
    shapes = {}
    offset = self.request.get_range('offset', 0, default=0)
    for datum in dataQuery.fetch(20, offset):
      obj = {}
      if not datum.shape in shapes:
        shapes[datum.shape] = ShapeField.all().filter('shape =', datum.shape).fetch(50)
      for field in shapes[datum.shape]:
        try:
          obj[field.name] = getattr(datum, field.name)
        except AttributeError:
          obj[field.name] = None
      if len(obj) > 0:
        obj['shape'] = datum.shape
        obj['id'] = datum.key().id()
        data.append(obj)
    self.success({'data': data})

class DataElement(Handler):
  #override
  def jsonPost(self, body, shape, _):
    if len(body.keys()) == 0:
      self.fail("no fields")
    else:
      query = ShapeField.all().filter('shape =', shape)
      if query.count() == 0:
        self.error(404)
      else:
        datum = Datum(shape=shape)
        fields = body.keys()
        valid = True
        for field in query.fetch(50):
          if field.name in fields:
            if not field.validInput(body[field.name]):
              valid = False
              self.fail("bad input for " + field.name)
              break
            setattr(datum, field.name, body[field.name])
          elif field.required:
            valid = False
            self.fail(field.name + " is a required field")
            break
          else:
            setattr(datum, field.name, None)
        if valid:
          datum.put()
          result = {"id": datum.key().id()}
          self.success(result)
  #override
  def jsonGet(self, shape, _):
    fields = ShapeField.all().filter('shape =', shape).fetch(50)
    if len(fields) == 0:
      self.error(404)
    else:
      dataQuery = Datum.all().filter('shape =', shape)
      data = []
      offset = self.request.get_range('offset', 0, default=0)
    for datum in dataQuery.fetch(20, offset):
      obj = {}
      for field in fields:
        try:
          obj[field.name] = getattr(datum, field.name)
        except AttributeError:
          obj[field.name] = None
      obj['shape'] = datum.shape
      obj['id'] = datum.key().id()
      data.append(obj)
    self.success({'data': data})

class DataSubelement(Handler):
  def __byShapeKey(self, shape, key):
    fields = ShapeField.all().filter('shape =', shape).fetch(50)
    try:
      key = int(key)
    except ValueError:
      return (None, fields)
    datum = Datum.get_by_id(key)
    if len(fields) == 0 or not datum or datum.shape != shape:
      return (None, fields)
    return (datum, fields)
  #override
  def jsonGet(self, shape, key):
    (datum, fields) = self.__byShapeKey(shape, key)
    if not datum:
      self.error(404)
    else:
      obj = {}
      for field in fields:
        try:
          obj[field.name] = getattr(datum, field.name)
        except AttributeError:
          obj[field.name] = None
      obj['shape'] = datum.shape
      obj['id'] = datum.key().id()
      self.success(obj)
  #override
  def jsonDelete(self, shape, key):
    (datum, fields) = self.__byShapeKey(shape, key)
    if not datum:
      self.error(404)
    else:
      datum.delete()
      self.success()
  #override
  def jsonPut(self, body, shape, key):
    (datum, fields) = self.__byShapeKey(shape, key)
    if not datum:
      self.error(404)
    else:
      keys = body.keys()
      valid = True
      for field in fields:
        if field.name in keys:
          if not field.validInput(body[field.name]):
            valid = False
            self.fail("bad input for " + field.name)
            break
          setattr(datum, field.name, body[field.name])
      if valid:
        datum.put()
        self.success()
application = webapp.WSGIApplication([
  ('/data', Data),
  (r'/data/(.*)/(.*)', DataSubelement),
  (r'/data/(.*)', DataElement)
  ], debug=True)

def main():
  run_wsgi_app(application)
if __name__ == "__main__":
  main()

