import unittest
from common import Server

class TestData(unittest.TestCase):
  def setUp(self):
    self.proxy = Server()
    (success, body) = self.proxy.put("shape/pet", {"name": {"type": "string"}})
    self.assertTrue(success)
  def tearDown(self):
    (success, body) = self.proxy.delete("shape/pet")
    self.assertTrue(success)
  def test_retrieve(self):
    (success, body) = self.proxy.post("data/pet", {"name": "Spot"})
    self.assertTrue(success)
    self.assertTrue('id' in body)
    self.assertTrue(isinstance(body['id'], int))
    dataId = body['id']

    moreData = True
    offset = 0
    while moreData:
      (success, body) = self.proxy.get("data?offset=" + str(offset))
      self.assertTrue(success)
      self.assertTrue('data' in body)
      for datum in body['data']:
        self.assertTrue('id' in datum)
        self.assertTrue('shape' in datum)
        if datum['id'] == dataId:
          self.assertTrue('name' in datum)
          self.assertEqual(datum['shape'], 'pet')
          self.assertEqual(datum['name'], 'Spot')
          moreData = False
          break
      if moreData and len(body['data']) == 20:
        offset = offset + 20

    (success, body) = self.proxy.delete("data/pet/" + str(dataId))
    self.assertTrue(success)
class TestDataElement(unittest.TestCase):
  def setUp(self):
    self.proxy = Server()
    (success, body) = self.proxy.put("shape/pet", {"name": {"type": "string"}})
    self.assertTrue(success)
  def tearDown(self):
    (success, body) = self.proxy.delete("shape/pet")
    self.assertTrue(success)
  def test_retrieve_invalid(self):
    """Try to retrieve on element which do not exist"""
    (success, body) = self.proxy.get("data/sdsdfdsfsdfds")
    self.assertFalse(success)
  def test_retrieve(self):
    (success, body) = self.proxy.post("data/pet", {"name": "Spot"})
    self.assertTrue(success)
    self.assertTrue('id' in body)
    self.assertTrue(isinstance(body['id'], int))
    dataId = body['id']

    moreData = True
    offset = 0
    while moreData:
      (success, body) = self.proxy.get("data/pet?offset=" + str(offset))
      self.assertTrue(success)
      self.assertTrue('data' in body)
      for datum in body['data']:
        self.assertTrue('id' in datum)
        self.assertTrue('shape' in datum)
        if datum['id'] == dataId:
          self.assertTrue('name' in datum)
          self.assertEqual(datum['shape'], 'pet')
          self.assertEqual(datum['name'], 'Spot')
          moreData = False
          break
      if moreData and len(body['data']) == 20:
        offset = offset + 20

    (success, body) = self.proxy.delete("data/pet/" + str(dataId))
    self.assertTrue(success)
  def test_create_not_valid(self):
    """ Cannot create with no fields"""
    (success, body) = self.proxy.post("data/pet", {})
    self.assertFalse(success)
    (success, body) = self.proxy.post("data/pet", {"otherfield": "bob"})
    self.assertFalse(success)
    (success, body) = self.proxy.post("data/pet", {"name": 123})
    self.assertFalse(success)
  def test_create(self):
    (success, body) = self.proxy.post("data/pet", {"name": "Spot", "otherfield": "value"})
    self.assertTrue(success)
    self.assertTrue('id' in body)
    self.assertTrue(isinstance(body['id'], int))
    dataId = body['id']

    (success, body) = self.proxy.get("data/pet/" + str(dataId))
    self.assertTrue(success)
    self.assertTrue('id' in body)
    self.assertTrue('shape' in body)
    self.assertTrue('name' in body)
    self.assertFalse('otherfield' in body)
    self.assertEqual(body['id'], dataId)
    self.assertEqual(body['shape'], 'pet')
    self.assertEqual(body['name'], 'Spot')

    (success, body) = self.proxy.delete("data/pet/" + str(dataId))
    self.assertTrue(success)
class TestDataSubelement(unittest.TestCase):
  def setUp(self):
    self.proxy = Server()
    (success, body) = self.proxy.put("shape/pet", {"name": {"type": "string"}})
    self.assertTrue(success)
    (success, body) = self.proxy.post("data/pet", {"name": "Spot"})
    self.assertTrue(success)
    self.assertTrue('id' in body)
    self.dataId = body['id']
  def tearDown(self):
    (success, body) = self.proxy.delete("data/pet/" + str(self.dataId))
    self.assertTrue(success)
    (success, body) = self.proxy.delete("shape/pet")
    self.assertTrue(success)
  def test_retrieve_invalid(self):
    """Try to retrieve on ids that do not exist"""
    (success, body) = self.proxy.get("data/pet/aaaaaa")
    self.assertFalse(success)
    (success, body) = self.proxy.get("data/pet/999999999999")
    self.assertFalse(success)
  def test_retrieve(self):
    (success, body) = self.proxy.get("data/pet/" + str(self.dataId))
    self.assertTrue(success)
    self.assertTrue('id' in body)
    self.assertTrue('shape' in body)
    self.assertTrue('name' in body)
    self.assertEqual(body['id'], self.dataId)
    self.assertEqual(body['shape'], 'pet')
    self.assertEqual(body['name'], 'Spot')
  def test_update_valid(self):
    """ Cannot create with no fields"""
    (success, body) = self.proxy.put("data/pet/" + str(self.dataId), {})
    self.assertFalse(success)
    (success, body) = self.proxy.put("data/pet/" + str(self.dataId), {"otherfield": "bob"})
    self.assertFalse(success)
    (success, body) = self.proxy.put("data/pet/" + str(self.dataId), {"name": 123})
    self.assertFalse(success)
  def test_update(self):
    """Can update if correct"""
    (success, body) = self.proxy.put("data/pet/" + str(self.dataId), {"name": "Shiloh", "otherfield": "value"})
    self.assertTrue(success)

    (success, body) = self.proxy.get("data/pet/" + str(self.dataId))
    self.assertTrue(success)
    self.assertTrue('id' in body)
    self.assertTrue('shape' in body)
    self.assertTrue('name' in body)
    self.assertFalse('otherfield' in body)
    self.assertEqual(body['id'], self.dataId)
    self.assertEqual(body['shape'], 'pet')
    self.assertEqual(body['name'], 'Shiloh')
  def test_delete_invalid(self):
    """Cannot delete an element which does not exist"""
    (success, body) = self.proxy.delete("data/pet/aaaaaa")
    self.assertFalse(success)
    (success, body) = self.proxy.delete("data/pet/999999999999")
    self.assertFalse(success)
  def test_delete(self):
    """Successful deletion"""
    (success, body) = self.proxy.post("data/pet", {"name": "Tim"})
    self.assertTrue(success)
    self.assertTrue('id' in body)
    dataId = body['id']
    (success, body) = self.proxy.get("data/pet/" + str(dataId))
    self.assertTrue(success)

    (success, body) = self.proxy.delete("data/pet/" + str(dataId))
    self.assertTrue(success)

    (success, body) = self.proxy.get("data/pet/" + str(dataId))
    self.assertFalse(success)
if __name__ == '__main__':
  unittest.main()
