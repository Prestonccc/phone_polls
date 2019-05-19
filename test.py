import unittest
import os
from time import sleep
from selenium import webdriver

from app import app, db
from app.models import Post, User


class TestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        db.init_app(app)
        self.username = '123'
        self.password = '123'
        self.email = '123@123.com'
        self.driver.maximize_window()

    def tearDown(self):
        if self.driver:
            self.driver.close()
        db.session.remove()

    def test_register(self):
        self.driver.get('http://127.0.0.1:5000/register')
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('email').send_keys(self.email)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_name('password2').send_keys(self.password)
        sleep(1)
        self.driver.find_element_by_name('submit').click()
        sleep(1)
        title = self.driver.title
        self.assertEqual('Sign In - Phone Polls', title)

    def test_login(self):
        self.login()

        logout = self.driver.find_element_by_name('logout').text
        self.assertEqual(logout, 'Logout', 'login success!')

    def test_edit(self):
        self.login()

        self.driver.find_element_by_name('profile').click()
        sleep(1)

        self.driver.find_element_by_name('edit').click()
        sleep(1)

        about_me = 'hello this is test'
        self.driver.find_element_by_name('about_me').clear()
        self.driver.find_element_by_name('about_me').send_keys(about_me)
        sleep(1)

        self.driver.find_element_by_name('submit').click()
        sleep(2)

        now_about = self.driver.find_element_by_id('about').text

        self.assertEqual(now_about, about_me, 'edit about_me success!')
        self.logout()

    def test_logout(self):
        self.login()

        self.driver.find_element_by_name('logout').click()
        sleep(1)
        try:
            login = self.driver.find_element_by_name('login')
            self.assertEqual(login.text, 'Login', 'logout success!')
        except BaseException as e:
            print(e)

    def test_post(self):
        self.login()

        post = 'hi i am test!'
        self.driver.find_element_by_name('post_text').send_keys(post)

        self.driver.find_element_by_id('post').click()
        sleep(1)

        last_post = self.driver.find_element_by_css_selector('.post-list p:last-child').text
        last_post = last_post.split(':')[1].strip()
        sleep(1)
        self.assertEqual(last_post, post, 'post success!')
        self.logout()

    def login(self):
        self.driver.get('http://localhost:5000/login')
        user = self.driver.find_element_by_name('username')
        user.send_keys(self.username)

        passwd = self.driver.find_element_by_name('password')
        passwd.send_keys(self.password)

        sleep(1)

        submit = self.driver.find_element_by_name('submit')
        submit.click()

        sleep(1)

    def logout(self):
        self.driver.get('http://localhost:5000')
        self.driver.find_element_by_name('logout').click()
        sleep(1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
