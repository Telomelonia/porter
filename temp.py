from porter_api import PorterAPI

porter = PorterAPI(name="Arjun Rampal", phone="9876546843", headless=False)

quote = porter.get_quote(
    pickup_address="Koramangala, Bangalore",
    drop_address="Electronic City, Bangalore",
    city="Bangalore",
    service_type="trucks"  # "trucks", "two_wheelers", or "packers_and_movers"
)

print(quote)