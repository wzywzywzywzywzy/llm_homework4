import unittest
from app.core.config import settings

class TestConfig(unittest.TestCase):
    def test_database_url(self):
        self.assertEqual(settings.DATABASE_URL, "sqlite:///./travel_planner.db")

    def test_algorithm(self):
        self.assertEqual(settings.ALGORITHM, "HS256")

if __name__ == '__main__':
    unittest.main()