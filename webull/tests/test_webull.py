import pytest
import webull

# pip install -U pytest
# python -m pytest -s

class TestUserClass:
    def test_login(self):
        webull_obj = webull.webull()
        assert True == webull_obj.login_prompt()

    def test_logout(self):
        webull_obj = webull.webull()
        print("Login success: {}".format(webull_obj.login_prompt()))
        assert True == webull_obj.logout()
