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
  def fromDict(self, form, field, update=False):
    #todo: update
    if not ('type' in field and 'name' in field):
      raise FormFieldException('"type" and "name" must be in each field')
    elif not (isinstance(field['type'], unicode) and isinstance(field['name'], unicode)):
      raise FormFieldException('"type" and "name" must both be strings')
    elif not field['type'].lower() in FormFieldTypes:
      raise FormFieldException('Invalid type. Can be one of: ' + ', '.join(FormFieldTypes))
    self.form = form
    self.name = field['name']
    self.fieldType = field['type']
    self.required = True
    return self
  #todo
  def deleteAndUpdate(self):
    self.delete()
    pass

class FormFieldException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
