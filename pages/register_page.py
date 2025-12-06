from pages.base_page import BasePage
from config.config import Config

class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def open(self):
        self.page.goto(Config.BASE_URL)

    def go_to_signup(self):
        self.page.get_by_role("button", name="Register free").click()

    
    def select_country(self, country: str):
        country_dropdown = self.page.locator("#clientreg_country-selctrl")
        country_dropdown.wait_for(state="visible")
        country_dropdown.click()
        # Wait for dropdown menu to open
        self.page.wait_for_timeout(500)
        # Try using select_option if it's a native select element
        try:
            self.page.select_option("#clientreg_country-selctrl", label=country)
        except:
            # If select_option doesn't work, it's likely a custom dropdown
            # Look for the option in the dropdown menu (could be in option tags or list items)
            # Try option element first - use filter approach
            try:
                select_element = self.page.locator("#clientreg_country-selctrl")
                country_option = select_element.locator("option").filter(has_text=country).nth(0)
                country_option.wait_for(state="attached", timeout=3000)
                country_option.click()
            except:
                # If option doesn't work, try finding by text in the visible dropdown menu
                # The dropdown might have opened a menu with the options
                self.page.get_by_text(country, exact=True).filter(
                    has=self.page.locator("option, li, [role='option']")
                ).nth(0).click()
    
    def select_random_country(self):
        """Select a random country from a predefined list"""
        import random
        # Common countries that are typically available in registration forms
        countries = [
            "Nepal", "United States", "United Kingdom", "India", "Canada", 
            "Australia", "Germany", "France", "Japan", "China", "Brazil", 
            "Mexico", "Spain", "Italy", "South Korea", "Netherlands", 
            "Sweden", "Norway", "Denmark", "Finland", "Poland", "Portugal"
        ]
        random_index = random.randint(0, len(countries) - 1)
        selected_country = countries[random_index]
        self.select_country(selected_country)
        return selected_country
        
    def select_month(self, month: int):
        """Select month from dropdown - accepts static value (1-12)"""
        month_dropdown = self.page.locator("#clientreg_dobmonth-selctrl")
        month_dropdown.wait_for(state="visible")
        month_dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try multiple approaches to find and select the month
        try:
            # First try: select by value
            self.page.select_option("#clientreg_dobmonth-selctrl", value=str(month))
        except:
            try:
                # Second try: select by label
                self.page.select_option("#clientreg_dobmonth-selctrl", label=str(month))
            except:
                # Third try: find option by text and click
                select_element = self.page.locator("#clientreg_dobmonth-selctrl")
                month_option = select_element.locator("option").filter(has_text=str(month)).first
                month_option.click()
    
    def select_day(self, day: int):
        """Select day from dropdown - accepts static value (1-31)"""
        day_dropdown = self.page.locator("#clientreg_dobday-selctrl")
        day_dropdown.wait_for(state="visible")
        day_dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try multiple approaches to find and select the day
        try:
            self.page.select_option("#clientreg_dobday-selctrl", value=str(day))
        except:
            try:
                self.page.select_option("#clientreg_dobday-selctrl", label=str(day))
            except:
                select_element = self.page.locator("#clientreg_dobday-selctrl")
                day_option = select_element.locator("option").filter(has_text=str(day)).first
                day_option.click()
    
    def select_year(self, year: int):
        """Select year from dropdown - accepts static value (e.g., 1990)"""
        year_dropdown = self.page.locator("#clientreg_dobyear-selctrl")
        year_dropdown.wait_for(state="visible")
        year_dropdown.click()
        self.page.wait_for_timeout(500)
        
        # Try multiple approaches to find and select the year
        try:
            self.page.select_option("#clientreg_dobyear-selctrl", value=str(year))
        except:
            try:
                self.page.select_option("#clientreg_dobyear-selctrl", label=str(year))
            except:
                select_element = self.page.locator("#clientreg_dobyear-selctrl")
                year_option = select_element.locator("option").filter(has_text=str(year)).first
                year_option.click()

    # def enter_dob(self, day: int = None, month: int = None, year: int = None):
    #     """
    #     Enter date of birth
    #     Args:
    #         day: Day of month (1-31), optional - defaults to random if not provided
    #         month: Month (1-12), optional - defaults to random if not provided
    #         year: Year, optional - defaults to random if not provided
    #     """
    #     import random
    #     from datetime import datetime
        
    #     # Generate random values if not provided
    #     if day is None:
    #         day = random.randint(1, 28)
    #     if month is None:
    #         month = random.randint(1, 12)
    #     if year is None:
    #         current_year = datetime.now().year
    #         year = random.randint(current_year - 65, current_year - 18)
        
    #     # Select month
    #     month_select = self.page.locator("[id*='dobMonth'], select[name*='month']").first
    #     month_select.wait_for(state="visible")
    #     try:
    #         month_select.select_option(label=str(month))
    #     except:
    #         month_select.select_option(value=str(month))
        
    #     # Select day
    #     day_select = self.page.locator("#clientreg_dobday-selctrl, [id*='dobday'], select[name*='day']").first
    #     day_select.wait_for(state="visible")
    #     try:
    #         day_select.select_option(label=str(day))
    #     except:
    #         day_select.select_option(value=str(day))
        
    #     # Select year
    #     year_select = self.page.locator("[id*='dobYear'], select[name*='year']").first
    #     year_select.wait_for(state="visible")
    #     try:
    #         year_select.select_option(label=str(year))
    #     except:
    #         year_select.select_option(value=str(year))
    def click_next(self):
        self.page.click("#countryDobNextBtn")

    def enter_email(self, email: str):
        self.page.fill("#email", email)
        self.page.keyboard.press("Tab") 
    
    def send_otp(self):
        self.page.click("#basicInfoNextBtn")

    def enter_password(self, password: str):
        self.page.fill("#password", password)

    def submit(self):
        self.page.click("button[type=submit]")

    def enter_verification_code(self, code: str):
        self.page.fill("#verification-code", code)

    def click_verify(self):
        self.page.click("#verify-button")