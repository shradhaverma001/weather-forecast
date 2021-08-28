import unittest
from weather_forecast import Today, History

class SimpleTest(unittest.TestCase):

	def test_lat(self):
		today = Today(28.535, 77.3912)		
		self.assertTrue(today.is_valid_lat(),True)

	def test_lon(self):
		today = Today(28.535, 77.3912)
		self.assertTrue(today.is_valid_lon(),True)

	def test_city(self):
		history = History("Noida", "2021-08-27")
		self.assertTrue(history.is_valid_city(), True)

	def test_date(self):
		history = History("Noida", "2021-08-27")
		self.assertTrue(history.is_valid_date(),True)

if __name__ == '__main__':
	unittest.main()
