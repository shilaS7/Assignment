from pages.base_page import BasePage
from config.config import Config

class LoginPage(BasePage):
    username_field = "input[name='username']"
    password_field = "input[name='password']"
    login_button = "button[type='submit']"

    def open(self):
        self.navigate(Config.BASE_URL)
    def go_to_login(self):
        self.page.get_by_role("button", name="Login").click()
    
    def login(self, username: str, password: str):
        self.page.fill(self.username_field, username)
        self.page.fill(self.password_field, password)
        self.page.click(self.login_button)