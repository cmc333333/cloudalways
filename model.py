from google.appengine.ext import db
from google.appengine.api import users

class Datum(db.Expando):
  #user = db.UserProperty()
  shape = db.StringProperty()

ShapeFieldTypes = ["string"]

class ShapeField(db.Model):
  shape = db.StringProperty()
  name = db.StringProperty()
  fieldType = db.StringProperty()
  required = db.BooleanProperty()
  def validInput(self, value):
    if self.fieldType == 'string':
      return isinstance(value, unicode)
    return False
  #todo
  def updateType(self, newType):
    fieldType = newType
    return self

class ShapeFieldException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
