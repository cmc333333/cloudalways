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
if __name__ == '__main__':
  unittest.main()
