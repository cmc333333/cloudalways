import unittest
from common import Server

class TestForm(unittest.TestCase):
  def setUp(self):
    self.proxy = Server()
  def test_post(self):
    (success, body) = self.proxy.post("form", {})
    self.assertFalse(success)
  def test_retrieve(self):
    (success, body) = self.proxy.put("form/person", {"first" : {"type": "string"}, "last": {"type": "string"}})
    self.assertTrue(success)
    (success, body) = self.proxy.put("form/pet", {"name": {"type": "string"}})
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

class TestFormElement(unittest.TestCase):
  def setUp(self):
    self.proxy = Server()
  def test_put_no_body(self):
    """Creation with no body should return an error"""
    (success, body) = self.proxy.put("form/person")
    self.assertFalse(success)
    (success, body) = self.proxy.put("form/person", {})
    self.assertFalse(success)
  def test_put_bad_fields(self):
    """Creation with bad fields"""
    (success, body) = self.proxy.put("form/person", {"name": "something"})
    self.assertFalse(success)
    (success, body) = self.proxy.put("form/person", {"name": {"type": "string"}, "other": 2})
    self.assertFalse(success)
  def test_put(self):
    """Successful creation"""
    (success, body) = self.proxy.put("form/person", {"first": {"type": "string"}, "last": {"type": "string"}})
    self.assertTrue(success)

    (success, body) = self.proxy.delete("form/person")
    self.assertTrue(success)

if __name__ == '__main__':
  unittest.main()
