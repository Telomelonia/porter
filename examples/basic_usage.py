from porter_api import PorterAPI, get_porter_quote

# Example 1: Using the PorterAPI class
porter = PorterAPI(name="John Doe", phone="9876543210")
quote = porter.get_quote(
    pickup_address="Koramangala, Bangalore",
    drop_address="Electronic City, Bangalore",
    city="Bangalore",
    service_type="trucks"
)
print("Class API result:", quote)

# Example 2: Using the convenience function
quote2 = get_porter_quote(
    name="Jane Smith",
    phone="9876543210",
    pickup_address="Bandra, Mumbai",
    drop_address="Andheri, Mumbai",
    city="Mumbai",
    service_type="two_wheelers"
)
print("Convenience function result:", quote2)
