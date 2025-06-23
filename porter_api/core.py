import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from .models import VehicleQuote
from .exceptions import PorterAPIError

def _validate_phone(phone: str) -> str:
    if not re.fullmatch(r"\d{10}", phone):
        raise PorterAPIError("Phone number must be exactly 10 digits.")
    return phone

def _parse_price_range(price_text: str) -> Tuple[Optional[int], Optional[int]]:
    match = re.findall(r"\d+", price_text.replace(",", ""))
    if len(match) == 2:
        return int(match[0]), int(match[1])
    elif len(match) == 1:
        return int(match[0]), int(match[0])
    return None, None

def _parse_capacity(capacity_text: str) -> Optional[int]:
    match = re.search(r"(\d+)", capacity_text.replace(",", ""))
    return int(match.group(1)) if match else None

class PorterAPI:
    SUPPORTED_CITIES = [
        "Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune"
    ]
    SERVICE_TYPES = ["two_wheelers", "trucks", "packers_and_movers"]

    def __init__(self, name: str, phone: str, headless: bool = True):
        self.name = name
        self.phone = _validate_phone(phone)
        self.headless = headless

    def get_supported_cities(self) -> List[str]:
        return self.SUPPORTED_CITIES

    def get_supported_service_types(self) -> List[str]:
        return self.SERVICE_TYPES

    def get_quote(self, pickup_address: str, drop_address: str, city: str, service_type: str = "trucks") -> Dict:
        if city not in self.SUPPORTED_CITIES:
            raise PorterAPIError(f"City '{city}' is not supported.")
        if service_type not in self.SERVICE_TYPES:
            raise PorterAPIError(f"Service type '{service_type}' is not supported.")

        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        # Use Service object for correct Chrome initialization
        from selenium.webdriver.chrome.service import Service
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 15)
        try:
            driver.get("https://porter.in/")
            # Select city
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "CitySelector_city-selected-text__1dNz4"))).click()
            city_elements = driver.find_elements(By.CSS_SELECTOR, '[class^="CitySelectorModal_city-title"]')
            found = False
            for el in city_elements:
                if city.lower() in el.text.lower():
                    el.click()
                    found = True
                    break
            if not found:
                raise PorterAPIError(f"City '{city}' not found on Porter.in.")
            # Open estimate form
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "EstimateCard_estimate-card__NgFIr"))).click()
            # Select service type
            radio_buttons = driver.find_elements(By.CLASS_NAME, "FareEstimateRequirement_requirement-radio-button__oBz_y")
            idx = self.SERVICE_TYPES.index(service_type)
            radio_buttons[idx].click()
            # Fill form fields
            pickup_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter pickup address"]')))
            pickup_input.clear()
            pickup_input.send_keys(pickup_address)
            drop_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter drop address"]')
            drop_input.clear()
            drop_input.send_keys(drop_address)
            mobile_input = driver.find_element(By.CSS_SELECTOR, '.FareEstimateForms_mobile-input__jy5wR')
            mobile_input.clear()
            mobile_input.send_keys(self.phone)
            name_input = driver.find_element(By.CSS_SELECTOR, '.FareEstimateForms_name-input__n8xyD')
            name_input.clear()
            name_input.send_keys(self.name)
            # Submit form
            submit_btn = driver.find_element(By.CSS_SELECTOR, '.FormInput_submit__ea0jJ.FormInput_submit-enabled__DbSnE.FareEstimateForms_submit-container___lB5u')
            submit_btn.click()
            # Wait for results
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'FareEstimateResultVehicleCard_container__BdMav')))
            result_cards = driver.find_elements(By.CLASS_NAME, 'FareEstimateResultVehicleCard_container__BdMav')
            quotes = []
            for card in result_cards:
                try:
                    vehicle_name = card.find_element(By.CLASS_NAME, 'FareEstimateResultVehicleCard_vehicle-name__d4107').text
                    price_text = card.find_element(By.CSS_SELECTOR, '.FareEstimateResultVehicleCard_vehicle-fare__3YMOc p').text
                    min_price, max_price = _parse_price_range(price_text)
                    capacity = card.find_element(By.CLASS_NAME, 'VehicleCapacity_vehicle-capacity__P53Z0').text
                    capacity_kg = _parse_capacity(capacity)
                    quotes.append({
                        "vehicle_name": vehicle_name,
                        "price_range": price_text,
                        "min_price": min_price,
                        "max_price": max_price,
                        "capacity": capacity,
                        "capacity_kg": capacity_kg
                    })
                except Exception:
                    continue
            return {
                "success": True,
                "pickup_address": pickup_address,
                "drop_address": drop_address,
                "city": city,
                "service_type": service_type,
                "user_name": self.name,
                "user_phone": self.phone,
                "quotes": quotes,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except (TimeoutException, NoSuchElementException) as e:
            return {
                "success": False,
                "error": str(e),
                "details": "Automation failed. Please check input and try again."
            }
        finally:
            driver.quit()

def get_porter_quote(name: str, phone: str, pickup_address: str, drop_address: str, city: str, service_type: str = "trucks") -> Dict:
    api = PorterAPI(name=name, phone=phone)
    return api.get_quote(pickup_address, drop_address, city, service_type)
