# porter-api-unofficial

Unofficial Python package to automate Porter.in delivery quote retrieval using Selenium.

## Features

- Get delivery quotes and vehicle capacity info from Porter.in
- Clean API for developers
- Robust error handling and type hints
- Educational/research use only (see disclaimer)

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from porter_api import PorterAPI, get_porter_quote

# Using the class
porter = PorterAPI(name="John Doe", phone="9876543210")
quote = porter.get_quote(
    pickup_address="Koramangala, Bangalore",
    drop_address="Electronic City, Bangalore",
    city="Bangalore",
    service_type="trucks"
)

# Using the convenience function
quote = get_porter_quote(
    name="Jane Smith",
    phone="9876543210",
    pickup_address="Bandra, Mumbai",
    drop_address="Andheri, Mumbai",
    city="Mumbai",
    service_type="two_wheelers"
)
```

## API Reference

See `porter_api/core.py` for full API details.

## Disclaimer

This is an unofficial, educational tool. It is not affiliated with or endorsed by Porter.in. Use responsibly and respect Porter's Terms of Service. Do not use for commercial purposes. The authors are not responsible for misuse.

## Supported Cities

- Bangalore
- Mumbai
- Delhi
- Chennai
- Hyderabad
- Pune
- ... (see `PorterAPI.get_supported_cities()`)

## Contributing

Pull requests welcome! See CONTRIBUTING.md for guidelines.
