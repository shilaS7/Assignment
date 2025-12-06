from pages.login_page import LoginPage

def test_login(page):
    login_page = LoginPage(page)
    login_page.open()
    # assert page.url == "https://www.pogo.com/"
    # pass