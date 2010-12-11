import unittest
from common import Server

class TestForm(unittest.TestCase):
  def setUp(self):
    self.proxy = Server()
  def test_create_no_body(self):
    """Creation with no body should return an error"""
    (success, body) = self.proxy.post("form")
    self.assertFalse(success)
    (success, body) = self.proxy.post("form", {})
    self.assertFalse(success)
  def test_create_no_name(self):
    """Creation with no name should return an error"""
    (success, body) = self.proxy.post("form", {"fields": [{"name": "first", "type": "string"}]})
    self.assertFalse(success)
  def test_create_no_fields(self):
    """Creation with no fields should return an error"""
    (success, body) = self.proxy.post("form", {"name": "person"})
    self.assertFalse(success)
  def test_create_bad_fields(self):
    """Creation with bad fields"""
    (success, body) = self.proxy.post("form", {"name": "person", "fields": "something"})
    self.assertFalse(success)
    (success, body) = self.proxy.post("form", {"name": "person", "fields": {"name": "first", "type": "string"}})
    self.assertFalse(success)
    (success, body) = self.proxy.post("form", {"name": "person", "fields": ["something"]})
    self.assertFalse(success)
    (success, body) = self.proxy.post("form", {"name": "person", "fields": [{"name": "first"}]})
    self.assertFalse(success)
    (success, body) = self.proxy.post("form", {"name": "person", "fields": [{"name": "first", "type": "string"},
      {"name": "last"}]})
    self.assertFalse(success)
  def test_create(self):
    """Successful creation"""
    (success, body) = self.proxy.post("form", {"name": "person", "fields": [{"name": "first", "type": "string"},
      {"name": "last", "type": "string"}]})
    self.assertTrue(success)
    self.assertTrue('name' in body)
    self.assertEqual(body['name'], 'person')

    (success, body) = self.proxy.delete("form/person")
    self.assertTrue(success)
  def test_create_duplicates(self):
    """Try to create duplicate form"""
    (success, body) = self.proxy.post("form", {"name": "pet", "fields": [{"name": "name", "type": "string"}]})
    self.assertTrue(success)
    (success, body) = self.proxy.post("form", {"name": "pet", "fields": [{"name": "name", "type": "string"}]})
    self.assertFalse(success)

    (success, body) = self.proxy.delete("form/pet")
    self.assertTrue(success)
  def test_retrieve(self):
    (success, body) = self.proxy.post("form", {"name": "person", "fields": [{"name": "first", "type": "string"},
      {"name": "last", "type": "string"}]})
    self.assertTrue(success)
    (success, body) = self.proxy.post("form", {"name": "pet", "fields": [{"name": "name", "type": "string"}]})
    self.assertTrue(success)
    (success, body) = self.proxy.get("form")
    self.assertTrue(success)
    self.assertTrue("person" in body)
    self.assertTrue("first" in body["person"])
    self.assertTrue("type" in body["person"]["first"])
    self.assertEqual(body["person"]["first"]["type"], "string")
    self.assertTrue("last" in body["person"])
    self.assertTrue("type" in body["person"]["last"])
    self.assertEqual(body["person"]["last"]["type"], "string")
    self.assertTrue("pet" in body)
    self.assertTrue("name" in body["pet"])
    self.assertTrue("type" in body["pet"]["name"])
    self.assertEqual(body["pet"]["name"]["type"], "string")

    (success, body) = self.proxy.delete("form/person")
    self.assertTrue(success)
    (success, body) = self.proxy.delete("form/pet")
    self.assertTrue(success)
  def test_update(self):
    (success, body) = self.proxy.put("form", {})
    self.assertFalse(success)
  def test_delete(self):
    (success, body) = self.proxy.delete("form")
    self.assertFalse(success)

if __name__ == '__main__':
  unittest.main()
