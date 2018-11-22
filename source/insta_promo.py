import json
import logging
import random
import subprocess
import time

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from exceptions.exceptions import LoginException

logging.basicConfig(filename="insta-logs.log",
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%b-%y %H:%M:%S')

BASE_URL = 'https://www.instagram.com'


class InstaPromo:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

    @staticmethod
    def get_tag():
        """Get a random tag from tags.txt file"""
        with open('tags.txt', 'r') as f:
            tags = list(f.readlines())
            i = random.randrange(len(tags))
        return tags[i].split('#')[-1].strip()

    @staticmethod
    def get_place():
        """Get a random geolocation from places.txt file"""
        with open('places.txt', 'r') as f:
            tags = list(f.readlines())
            i = random.randrange(len(tags))
        return tags[i]

    @staticmethod
    def get_credentials():
        """Get username and password from config.json"""
        with open("config.json") as f:
            login_data = json.load(f)
        return login_data["username"], login_data["password"]

    def _disable_notifications(self):
        """Click 'Not now' to disable notifications after logging into an account"""
        not_now_button = WebDriverWait(self.driver, 15).until(
            lambda element: self.driver.find_element_by_xpath(
                "//div[@role='dialog']/div//following::div[2]//following::button[1]"))
        not_now_button.click()

    def login(self):
        """Perform logging to the site"""
        self.driver.get(f"{BASE_URL}/accounts/login/?hl=en")
        username, password = self.get_credentials()
        # webdriver's going to wait max 10 seconds for email's field, password field, login button to display
        username_element = WebDriverWait(self.driver, 10).until(
            lambda element: self.driver.find_element_by_name("username"))
        password_element = WebDriverWait(self.driver, 10).until(
            lambda element: self.driver.find_element_by_name("password"))
        try:
            username_element.clear()
            username_element.send_keys(username)
            password_element.clear()
            password_element.send_keys(password)
            login_button = WebDriverWait(self.driver, 10).until(
                lambda element: self.driver.find_element_by_xpath("//button[text()='Log in']"))
            login_button.click()
            print("Logged in.")
            logging.warning("Logged in.")
            time.sleep(random.randint(1, 5))
        except LoginException:
            logging.exception("Can't log in to the site. Please check your credentials!")

    def promote_via_tags(self):
        """Search posts by random tag, like posts and follow their owners"""
        tag = self.get_tag()
        time.sleep(random.randint(5, 10))
        print('#'+tag)
        logging.warning('#'+tag)
        url = f"{BASE_URL}/explore/tags/{tag}?hl=en"
        self._follow_like(url)

    def promote_via_location(self):
        """Search posts by location"""
        place = self.get_place()
        time.sleep(random.randint(5, 10))
        print(place.split('/')[-1].strip())
        logging.warning(place.split('/')[-1].strip())
        url = f"{BASE_URL}/explore/locations/{place}?hl=en"
        self._follow_like(url)

    def _follow_like(self, url):
        """Like posts and follow their owners"""
        for i in range(3):
            self.driver.get(url)
            time.sleep(random.randint(2, 5))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # random choice of picking most popular (1) or newest post (2) with preference to the second ones
            option = random.choice(['1'] * 5 + ['2'] * 30)
            post = self.driver.find_element_by_xpath(
                f"//article//following::div[{option}]/div/div/div[{i+1}]/a")
            post_url = post.get_attribute("href")
            logging.warning('Post url: ' + post_url[:-1])
            self.driver.get(post_url[:-1] + "?hl=en")
            try:
                # wait until presence of like button
                like = WebDriverWait(self.driver, 10).until(
                    lambda element: self.driver.find_element_by_xpath(
                        "//span[@aria-label='Like']"))
                like.click()
                print('\tLiked.')
                time.sleep(random.randint(3, 5))
                follow_button = self.driver.find_element_by_xpath("//button[text()='Follow']")
                follow_button.click()
                print('\tFollowed.')

                time.sleep(random.randint(5, 10))

                logging.warning('Followed and liked post.')
            # if user was followed, post was liked before for some reason
            except (NoSuchElementException, TimeoutException):
                e = 'Error following user/liking post. Perhaps it was already done.'
                print(e)
                logging.warning(e)

    def promote(self):
        """Main method"""
        quantity = random.randint(300, 400)
        for _ in range(quantity):
            self.promote_via_tags()
            self.promote_via_location()

        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.quit()


def kill_processes():
    """Killing processes to clean memory"""
    try:
        subprocess.call("killall chromium-browse", shell=True)
        subprocess.call("killall chromium-browser", shell=True)
        subprocess.call("killall chromedriver", shell=True)
    except subprocess.SubprocessError:
        pass


if __name__ == "__main__":
    kill_processes()

    promoter = InstaPromo()
    logging.warning("\n*** New bot session ***")
    promoter.login()
    promoter.promote()
