from google.appengine.ext import db
from google.appengine.api import users

class Datum(db.Expando):
  #user = db.UserProperty()
  form = db.StringProperty()

FormFieldTypes = ["string"]

class FormField(db.Model):
  form = db.StringProperty()
  name = db.StringProperty()
  fieldType = db.StringProperty()
  required = db.BooleanProperty()
  def setValidations(self, fieldType):
    fieldType = fieldType.lower()
    if fieldType == "string":
      self.validations = ['string']
  #todo
  def updateType(self, newType):
    fieldType = newType
    return self

class FormFieldException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
