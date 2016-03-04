
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Welcome to commuKNITty')

    def test_landing_page(self):
        self.browser.get('http://localhost:5000/')
        self.browser.find_element_by_id("nav-profile").click()
        self.assertIn("You are not authorized", self.browser.page_source)

    # def test_math(self):
    #     self.browser.get('http://localhost:5000/')
    #
    #     x = self.browser.find_element_by_id('x-field')
    #     x.send_keys("3")
    #     y = self.browser.find_element_by_id('y-field')
    #     y.send_keys("4")
    #
    #     btn = self.browser.find_element_by_id('calc-button')
    #     btn.click()
    #
    #     result = self.browser.find_element_by_id('result')
    #     self.assertEqual(result.text, "7")

    # def test_search_in_python_org(self):
    #     driver = self.driver
    #     driver.get("http://www.python.org")
    #     self.assertIn("Python", driver.title)
    #     elem = driver.find_element_by_name("q")
    #     elem.send_keys("pycon")
    #     elem.send_keys(Keys.RETURN)
    #     assert "No results found." not in driver.page_source


    # TESTS TO RUN:
    # landing page:
        # pre login, get not authorized flash message
        # click login

if __name__ == "__main__":
    unittest.main()
