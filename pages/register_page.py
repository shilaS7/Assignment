import random
import string
from pages.base_page import BasePage
from config.config import Config

class RegisterPage(BasePage):
    
    def __init__(self, page):
        super().__init__(page)
    
    def open(self):
        """Open the registration page."""
        self.page.goto(Config.BASE_URL)
    
    def go_to_signup(self):
        self.page.get_by_role("button", name="Register free").click()
    
    def select_country(self, country: str):
        dropdown = self.page.locator("#clientreg_country-selctrl")
        dropdown.wait_for(state="visible")
        dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try different methods to select country
        try:
            self.page.select_option("#clientreg_country-selctrl", label=country)
        except:
            try:
                dropdown.locator("option").filter(has_text=country).first.click()
            except:
                self.page.get_by_text(country, exact=True).first.click()
    
    def select_random_country(self):
        countries = [
            "Nepal", "United States", "United Kingdom", "India", "Canada",
            "Australia", "Germany", "France", "Japan", "China", "Brazil",
            "Mexico", "Spain", "Italy", "South Korea", "Netherlands",
            "Sweden", "Norway", "Denmark", "Finland", "Poland", "Portugal"
        ]
        country = random.choice(countries)
        self.select_country(country)
        print(f"🌍 Selected country: {country}")
        return country
    
    def _select_dropdown_option(self, selector: str, value: str):
        dropdown = self.page.locator(selector)
        dropdown.wait_for(state="visible")
        dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try different selection methods
        try:
            self.page.select_option(selector, value=value)
        except:
            try:
                self.page.select_option(selector, label=value)
            except:
                dropdown.locator("option").filter(has_text=value).first.click()
    
    def select_month(self, month: int):
        self._select_dropdown_option("#clientreg_dobmonth-selctrl", str(month))
    
    def select_day(self, day: int):
        self._select_dropdown_option("#clientreg_dobday-selctrl", str(day))
    
    def select_year(self, year: int):
        self._select_dropdown_option("#clientreg_dobyear-selctrl", str(year))
    
    def click_next(self):
        self.page.click("#countryDobNextBtn")
    
    def enter_email(self, email: str):
        field = self.page.locator("#email")
        field.wait_for(state="visible")
        field.fill(email)
        self.page.keyboard.press("Tab")
        print(f"📧 Email entered: {email}")
    
    def send_otp(self):
        print("📤 Sending OTP...")
        self.page.click("#basicInfoNextBtn")
        self.page.wait_for_timeout(2000)  # Wait for OTP to be sent
    
    def enter_verification_code(self, code: str):
        print(f"🔑 Entering verification code: {code}")

        field = self.page.locator("#emailVerifyCode")
        field.wait_for(state="visible", timeout=10000)
        field.fill(code)
        print("✅ Verification code entered")
    
    def send_verification_code(self):
        self.page.click("#btnSendCode")
        
    @staticmethod
    def generate_unique_ea_id() -> str:        # Generate 3 random digits
        random_digits = ''.join(random.choices(string.digits, k=3))
        ea_id = f"Bonsoir{random_digits}"
        print(f"🆔 Generated EA ID: {ea_id}")
        return ea_id
    def enter_ea_id(self, ea_id: str):
        self.page.fill("#originId", ea_id)
    def enter_password(self, password: str):
        self.page.fill("#password", password)
        self.page.keyboard.press("Tab")
    def click_terms_and_conditions(self):
        self.page.click("#read-accept-container")
    def click_create_account(self):
        self.page.click("#basicInfoNextBtn")
    def click_finish(self):
        self.page.click("#submitBtn")
    def click_next_to_login(self, button_name: str = "Next to Login"):
        self.page.get_by_role("button", name=button_name).click()