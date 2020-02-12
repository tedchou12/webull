import pytest
import getpass
import webull

# python -m pytest -s

class TestUserClass:
    def test_login(self):
        webull_obj = webull.webull()
        uname = input("Enter Webull Username:")
        pwd = getpass.getpass("Enter Webull Password:")
        assert True == webull_obj.login(uname, pwd)

    def test_logout(self):
        webull_obj = webull.webull()
        uname = input("Enter Webull Username:")
        pwd = getpass.getpass("Enter Webull Password:")
        print("Login success: {}".format(webull_obj.login(uname, pwd)))
        assert True == webull_obj.logout()
