""" Browser tests for the CommuKNITty webapp """

import unittest
from selenium import webdriver


class BrowserTest(unittest.TestCase):

    def setUp(self):
        """ Steps to run before every test """

        self.browser = webdriver.Firefox()

    def tearDown(self):
        """ Steps to run after every test """

        self.browser.quit()

    def test_title(self):
        """ Does title render for landing page? """

        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Welcome to commuKNITty')

    def test_landing_page(self):
        """ Does landing page render without logged in user? """

        self.browser.get('http://localhost:5000/')
        self.browser.find_element_by_id("nav-profile").click()
        self.assertIn("You are not authorized", self.browser.page_source)

    def test_login_modal(self):
        """ Does login window render when login button is clicked? """

        self.browser.get('http://localhost:5000/')
        login_button = self.browser.find_element_by_id("login-button")
        login_button.click()
        self.assertIn("Username:", self.browser.page_source)

    def test_login(self):
        """ Can the user log in? """

        self.browser.get('http://localhost:5000/')
        login_button = self.browser.find_element_by_id("login-button")
        login_button.click()
        username = self.browser.find_element_by_id("username-for-login")
        username.send_keys("rhymeswithcount")
        submit = self.browser.find_element_by_id("login-submit")
        submit.click()
        self.assertIn("Welcome, rhymeswithcount", self.browser.page_source)


def get_suite():

    suite = unittest.TestSuite()
    suite.addTest(BrowserTest("test_title"))
    suite.addTest(BrowserTest("test_landing_page"))
    suite.addTest(BrowserTest("test_login_modal"))
    suite.addTest(BrowserTest("test_login"))

    return suite


if __name__ == "__main__":
    unittest.main()
