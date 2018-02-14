# from django.test import TestCase
#
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
#
#
# class SeleniumTests(LiveServerTestCase):
#
#     def setUp(self):
#         self.selenium = webdriver.Firefox()
#         super(SeleniumTests, self).setUp()
#
#     def tearDown(self):
#         self.selenium.quit()
#         super(SeleniumTests, self).tearDown()
#
#     def test_register(self):
#         selenium = self.selenium
#         selenium.get('http://localhost:8000/planner/signup')
#
#         try:
#             element = WebDriverWait(selenium, 10).until(
#                 EC.presence_of_element_located((By.ID, "UserName"))
#             )
#         finally:
#             selenium.quit()
#
#         # find the form element
#         username = selenium.find_element_by_id('UserName')
#         email = selenium.find_element_by_id('MailAddress')
#         password1 = selenium.find_element_by_id('Password')
#
#         submit = selenium.find_element_by_name('SignUp')
#
#         # Fill the form with data
#         username.send_keys('jamesbond')
#         email.send_keys('james@bond.com')
#         password1.send_keys('123456')
#
#         # submitting the form
#         submit.send_keys(Keys.RETURN)
#         # check the returned result
#         assert "Index page" in selenium.title
