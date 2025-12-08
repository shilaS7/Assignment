from pages.base_page import BasePage
from config.config import Config

class LoginPage(BasePage):
    username_field = "input[name='username']"
    password_field = "input[name='password']"
    login_button = "button[type='submit']"

    def open(self):
        self.navigate(Config.BASE_URL)

    def go_to_login(self):
        self.page.get_by_role("button", name="Sign In").click()
    
    def enter_email(self, email: str):
        self.page.fill("#email", email)
    
    def click_next(self):
        self.page.click("#logInBtn")
    
    def enter_password(self, password: str):
        self.page.type("#password", password,delay=100)
        print(f"Typed password: {password}")
        self.page.keyboard.press("Tab")
    
    # def login(self, username: str, password: str):
    #     self.page.fill(self.username_field, username)
    #     self.page.fill(self.password_field, password)
    #     self.page.click(self.login_button)