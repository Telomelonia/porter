# porter-api-unofficial

🚛 **Because manually checking Porter quotes is so 2023**

_An unofficial Python package that automates Porter.in delivery quote retrieval using Selenium (and a sprinkle of magic)_

---

## 🎭 About This Little Project

Hey there! 👋 This is a fun little side project created by yours truly [@telomelonia](https://github.com/telomelonia) during one of those "I wonder if I can automate this" moments. You know the feeling, right?

**What it does:** Fetches delivery quotes from Porter.in faster than you can say "logistics"  
**What it doesn't do:** Your laundry (sadly)

---

## ⚠️ Important Disclaimers (The Boring But Necessary Stuff)

🎓 **Educational & Informational Use Only**

- This tool is purely for educational and research purposes
- Not affiliated with, endorsed by, or connected to Porter.in in any way
- Please respect Porter's Terms of Service and don't be _that_ person
- No commercial use - keep it cool, keep it educational

🤖 **Web Scraping Reality Check**

- This uses web automation (Selenium) which means it's as fragile as your New Year's resolutions
- Porter.in might change their website and break everything (it happens!)
- If something breaks, please don't panic - just [post an issue](https://github.com/telomelonia/porter/issues) and I'll fix it when I'm not binge-watching Netflix

---

## 🚀 Installation

```bash
# Clone this bad boy
git clone https://github.com/telomelonia/porter.git
cd porter

# Install dependencies (only 2, because I'm not a monster)
pip install -r requirements.txt
```

---

## 🎮 Quick Start (The Fun Part!)

```python
from porter_api import PorterAPI, get_porter_quote

# Method 1: The Classy OOP Way
porter = PorterAPI(name="John Doe", phone="9876543210")
quote = porter.get_quote(
    pickup_address="Koramangala, Bangalore",
    drop_address="Electronic City, Bangalore",
    city="Bangalore",
    service_type="trucks"  # because trucks are cool
)
print("Look ma, I got quotes!", quote)

# Method 2: The "I Just Want Results" Way
quote = get_porter_quote(
    name="Jane Smith",
    phone="9876543210",
    pickup_address="Bandra, Mumbai",
    drop_address="Andheri, Mumbai",
    city="Mumbai",
    service_type="two_wheelers"  # for when you're feeling speedy
)
print("Zoom zoom! 🏍️", quote)
```

---

## 📋 API Reference (The Technical Stuff)

### PorterAPI Class

```python
class PorterAPI:
    def __init__(self, name: str, phone: str, headless: bool = True)
    def get_quote(self, pickup_address: str, drop_address: str, city: str, service_type: str = "trucks") -> Dict
    def get_supported_cities() -> List[str]
    def get_supported_service_types() -> List[str]
```

### Response Format

When everything works perfectly (fingers crossed! 🤞):

```python
{
    'success': True,
    'pickup_address': 'Koramangala, Bangalore',
    'drop_address': 'Electronic City, Bangalore',
    'city': 'Bangalore',
    'service_type': 'trucks',
    'user_name': 'Arjun Rampal',
    'user_phone': '9876546843',
    'quotes': [
        {
            'vehicle_name': '3 Wheeler',
            'price_range': '₹585 - ₹615',
            'min_price': 585,
            'max_price': 615,
            'capacity': '500 kg',
            'capacity_kg': 500
        },
        # ... more awesome vehicles
    ],
    'timestamp': '2025-06-24 19:12:50'
}
```

When things go sideways (it happens to the best of us):

```python
{
    'success': False,
    'error': 'Something went wrong',
    'details': 'More details about what exploded',
    'suggestion': 'Try running again or check if Porter.in is having a bad day'
}
```

---

## 🌍 Supported Cities

- Bangalore (Namma Bengaluru! 🌆)
- Mumbai (The city that never sleeps)
- Delhi (Capital vibes)
- Chennai (Marina Beach logistics)
- Hyderabad (Biryani and deliveries)
- Pune (IT hub express)

_Want more cities? fork the repo and please help this poor guy's repo 🙏_

---

## 🚛 Service Types

- `"two_wheelers"` - For when you need speed over size
- `"trucks"` - The workhorses of logistics
- `"packers_and_movers"` - For when you're relocating your entire life

---

## 🐛 When Things Break (Error Handling)

This package includes robust error handling because, let's face it, automation is temperamental:

### Common Issues & Solutions

**🔧 "The website changed and everything broke!"**

- First, take a deep breath
- Try running your code again (sometimes it's just a hiccup)
- If it still doesn't work, [create an issue](https://github.com/telomelonia/porter/issues) with:
  - Your Python version
  - What you were trying to do
  - The error message (copy-paste is your friend)
  - Maybe a screenshot if you're feeling fancy

**📱 "Invalid phone number!"**

- It could be possible there backend engineer lock in
- Phone numbers should be exactly 10 digits
- No country codes, no spaces, no dashes - just pure digits

**🏙️ "City not supported!"**

- Check the supported cities list above
- Make sure you're spelling it correctly (case doesn't matter)

**🚛 "Service type not found!"**

- Use one of: "two_wheelers", "trucks", "packers_and_movers"
- Yes, underscores are important!

---

## 🤝 Contributing (Join the Fun!)

Found a bug? Want to add a feature? Think my code could be better? (It probably can be! 😅)

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request and describe what you did

---

## 🙋‍♂️ Support & Questions

- **Issues:** [GitHub Issues](https://github.com/telomelonia/porter/issues) (for bugs and feature requests)
- **Questions:** Also GitHub Issues (I'm not too cool for Q&A)
- **Random Chat:** Find me [@telomelonia](https://github.com/telomelonia) on GitHub

---

## 🎬 Final Notes

This project was built with ❤️, ☕, and probably too much GenAI. It's my small contribution to the "let's automate boring stuff" movement.

Remember: Use this responsibly, respect Porter.in's services! Enjoy...✨

---

_P.S. If this package saves you time, consider starring the repo ⭐ - it motivates me and costs you nothing!_

**Happy coding! 🎉**

---

_Made with 🔧 by [@telomelonia](https://github.com/telomelonia) | Not affiliated with Porter.in_
