import time, os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from .models import User, Post
from django.contrib.auth import get_user_model
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        log_dir = "/tmp/logs"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, 'chromedriver.log')

        chrome_options = Options()

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        cls.driver = webdriver.Chrome(service=Service(log_path=log_path), options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def create_account(self, username, email, password):
        self.driver.get("http://localhost:5173/signup")

        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys(username)

        email_field = self.driver.find_element(By.ID, "email")
        email_field.send_keys(email)

        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        submitBtn = self.driver.find_element(By.ID, "sign-up-btn")
        submitBtn.click()

    def test_sign_up(self):
        User = get_user_model()

        email = "myuser@gmail.com"
        username = "myuser"
        password = "password"

        test_user = User.objects.create_user(username=username, email=email, password=password)
        test_user.save()

        self.create_account(username=username, email=email, password=password)

    def login_account(self, username, password):
        self.driver.get("http://localhost:5173/login")

        username_element = self.driver.find_element(By.ID, "username")
        username_element.send_keys(username)

        password_element = self.driver.find_element(By.ID, "password")
        password_element.send_keys(password)

        loginBtn = self.driver.find_element(By.ID, "log-in-btn")
        loginBtn.click()
        time.sleep(2)

    def test_login(self):
        User = get_user_model()

        email = "myuser@gmail.com"
        username = "myuser"
        password = "password"

        test_user = User.objects.create_user(username=username, email=email, password=password)
        test_user.save()

        self.login_account(username, password)
        time.sleep(2)

    def test_create_post(self):
        self.test_login()

        modalBtn = self.driver.find_element(By.CLASS_NAME, "create-post-btn")
        modalBtn.click()

        title_field = self.driver.find_element(By.ID, "title")
        title_field.send_keys("Test")

        textarea_field = self.driver.find_element(By.ID, "content")
        textarea_field.send_keys("This is a short description")

        submitPostBtn = self.driver.find_element(By.CLASS_NAME, "submit-post-btn")
        submitPostBtn.click()
        time.sleep(1)


    # doesnt work - need to fix this 

    # def test_post_comment(self):
    #     self.test_create_post()
    #     time.sleep(2)

    #     post_card = self.driver.find_element(By.ID, "post-item")
    #     post_card.click()
    #     time.sleep(2)

    #     add_comment_button = self.driver.find_element(By.CLASS_NAME, "add-comment-btn")
    #     add_comment_button.click()
    #     time.sleep(1)

    #     content_field = self.driver.find_element(By.ID, "content")
    #     content_field.send_keys("This is a test comment.")

    #     submit_button = self.driver.find_element(By.ID, "submit-button")
    #     submit_button.click()
    #     time.sleep(2)

    #     close_modal_button = self.driver.find_element(By.ID, "close-button")
    #     close_modal_button.click()
    #     time.sleep(2)

    #     self.assertIn("This is a test comment.", self.driver.page_source)