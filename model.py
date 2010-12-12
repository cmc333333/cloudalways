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
  def pythonType(self):
    if self.fieldType == 'string':
      return unicode
    else:
      return None
  def setValidations(self, fieldType):
    fieldType = fieldType.lower()
    if fieldType == "string":
      self.validations = ['string']
  #todo
  def updateType(self, newType):
    fieldType = newType
    return self

class ShapeFieldException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
