import re
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
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

    def select_service_type(self, driver, wait, service_type: str) -> bool:
        """
        Select the service type on the Porter.in estimate form with debugging and robust error handling.
        """
        try:
            print("Looking for category selector...")
            
            # Wait for page to fully load
            time.sleep(3)
            
            # Service mapping
            service_mapping = {
                "two_wheelers": "Two Wheelers",
                "trucks": "Trucks", 
                "packers_and_movers": "Packers & Movers"
            }
            
            target_text = service_mapping.get(service_type, "Trucks")
            print(f"Looking for service: {target_text}")
            
            # Try to find category selector containers
            selectors_to_try = [
                "CategorySelector_category-select-container__LgXjx",
                "[class*='CategorySelector'][class*='container']",
                "[class*='category-select-container']",
                "[class*='category'][class*='container']"
            ]
            
            service_containers = []
            for selector in selectors_to_try:
                try:
                    if selector.startswith("["):
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    else:
                        elements = driver.find_elements(By.CLASS_NAME, selector)
                    print(f"Selector '{selector}': Found {len(elements)} elements")
                    if elements:
                        service_containers = elements
                        break
                except Exception as e:
                    print(f"Error with selector '{selector}': {e}")
            
            if not service_containers:
                print("No service containers found! Dumping page source...")
                print("Current URL:", driver.current_url)
                with open("porter_debug.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print("Page source saved to porter_debug.html")
                return False
            
            print(f"Found {len(service_containers)} service containers")
            
            # Look for the container with our target text
            for i, container in enumerate(service_containers):
                try:
                    # Get all text in this container
                    container_text = container.text
                    print(f"Container {i}: {container_text}")
                    
                    if target_text.lower() in container_text.lower():
                        print(f"Found target service in container {i}: {container_text}")
                        
                        # Try multiple click approaches
                        try:
                            # Method 1: Direct click on container
                            container.click()
                            print("Successfully clicked using direct click")
                            time.sleep(2)
                            return True
                            
                        except ElementClickInterceptedException:
                            print("Direct click intercepted, trying JavaScript click...")
                            
                            # Method 2: JavaScript click
                            driver.execute_script("arguments[0].click();", container)
                            print("Successfully clicked using JavaScript")
                            time.sleep(2)
                            return True
                            
                except Exception as e:
                    print(f"Error checking container {i}: {e}")
                    continue
                    
            print(f"Could not find service type: {target_text}")
            print("Available options were:")
            for i, container in enumerate(service_containers):
                try:
                    print(f"  {i}: {container.text}")
                except:
                    print(f"  {i}: Could not get text")
            
            return False
            
        except Exception as e:
            print(f"Error in select_service_type: {e}")
            return False

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
            
            # NEW: Select service type using the updated method
            if not self.select_service_type(driver, wait, service_type):
                return {
                    "success": False,
                    "error": f"Could not select service type: {service_type}",
                    "details": "Service selection failed"
                }
            
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
