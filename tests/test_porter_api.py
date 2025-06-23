import unittest
from porter_api import PorterAPI, get_porter_quote
from porter_api.exceptions import PorterAPIError

class TestPorterAPI(unittest.TestCase):
    def setUp(self):
        self.valid_name = "Test User"
        self.valid_phone = "9876543210"
        self.valid_city = "Bangalore"
        self.valid_service = "trucks"
        self.pickup = "Koramangala, Bangalore"
        self.drop = "Electronic City, Bangalore"

    def test_supported_cities(self):
        api = PorterAPI(self.valid_name, self.valid_phone)
        self.assertIn(self.valid_city, api.get_supported_cities())

    def test_invalid_phone(self):
        with self.assertRaises(PorterAPIError):
            PorterAPI(self.valid_name, "12345")

    def test_invalid_city(self):
        api = PorterAPI(self.valid_name, self.valid_phone)
        with self.assertRaises(PorterAPIError):
            api.get_quote(self.pickup, self.drop, "Atlantis", self.valid_service)

    def test_invalid_service_type(self):
        api = PorterAPI(self.valid_name, self.valid_phone)
        with self.assertRaises(PorterAPIError):
            api.get_quote(self.pickup, self.drop, self.valid_city, "invalid_service")

    def test_convenience_function(self):
        # This will actually run Selenium and may fail if site structure changes
        result = get_porter_quote(
            name=self.valid_name,
            phone=self.valid_phone,
            pickup_address=self.pickup,
            drop_address=self.drop,
            city=self.valid_city,
            service_type=self.valid_service
        )
        self.assertIn("success", result)

if __name__ == "__main__":
    unittest.main()
