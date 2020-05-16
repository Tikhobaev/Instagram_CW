import itertools
import random

import selenium
from selenium import webdriver
from explicit import waiter, XPATH
from selenium.webdriver.common.keys import Keys
import time
import psycopg2

QUICK_BREAK = 1
LONG_BREAK = 10
WAITING_TIME = 1.1
WAIT = 0.2
THRESHOLD = 30


class AccountDoesNotExist(Exception):
    pass


def select(cur, database):
    cur.execute(f"SELECT username FROM {database} LIMIT 1;")
    records = cur.fetchall()
    return records


def isInDatabase(cur, username, database):
    cur.execute(f"SELECT username FROM {database} WHERE username = '{username}';")
    records = cur.fetchall()
    return len(records) != 0


def insert(cur, con, username, database):
    cur.execute(f"INSERT INTO {database} (username) VALUES ('{username}');")
    con.commit()


def drop(cur, con, username, database):
    cur.execute(f"DELETE FROM {database} WHERE username = '{username}';")
    con.commit()


def insert_data(cur, con, database, user):
    cur.execute(f"""INSERT INTO {database} (
        username, 
        follower_count,
        following_count,
        media_count,
        name,
        biography,
        followers,
        followings,
        isPrivate) 
        VALUES (
        '{user.username}',
        '{user.follower_count}',
        '{user.following_count}',
        '{user.media_count}',
        '{user.name or 'NULL'}',
        '{user.biography or 'NULL'}',
        '{user.joined_followers or 'NULL'}',
        '{user.joined_followings or 'NULL'}',
        '{user.isPrivate}' );""")
    con.commit()


class User:
    def __init__(self, username):
        self.username = username
        self.follower_count = ''
        self.following_count = ''
        self.media_count = ''
        self.name = ''
        self.biography = ''
        self.followers = []
        self.followings = []
        self.isPrivate = False
        self.joined_followers = ''
        self.joined_followings = ''


class InstagramBot():
    def __init__(self, email, password):
        self.browser = webdriver.Chrome()
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(3 + random.random())
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(3 + random.random())

    def scrape_user(self, username):
        user = self.scrape_base(username)
        time.sleep(random.random())
        if not user.isPrivate:
            # self.scrape_media(user)
            if int(user.follower_count) <= 1000 and int(user.following_count) <= 1000:
                self.scrape_followers(user)
                time.sleep(1.5 + random.random() * 2)
                # exit followers window

                time.sleep(1.5 + random.random() * 3)
                self.scrape_followings(user)
        return user

    def scrape_followers(self, user: User):
        try:
            upper_buttons = self.browser.find_elements_by_class_name('-nal3 ')
            upper_buttons[1].click()
            waiter.find_element(self.browser, "//div[@role='dialog']", by=XPATH)
        except Exception as e:
            print(user.username, ' does not have followers')
            return
        followers = []
        follower_css = "ul div li:nth-child({}) a.notranslate"  #  Taking advange of CSS's nth-child functionality
        time.sleep(2 + random.random()*2)
        if int(user.follower_count) > 0:
            for follower_index in range(1, int(user.follower_count) + 1):
                try:
                    follower_index = str(follower_index)
                    followers.append(waiter.find_element(self.browser, follower_css.format(follower_index)).text)
                    if follower_index == user.follower_count:
                        break
                    if int(follower_index) % 4 == 0:
                        last_follower = waiter.find_element(self.browser, follower_css.format(follower_index))
                        self.browser.execute_script("arguments[0].scrollIntoView();", last_follower)
                        time.sleep(0.45 + random.random()*0.1)
                except Exception as e:
                    print(e)
                    break
        print('\tFollowers -', user.follower_count, 'scrapped: ', len(followers))
        user.followers = followers
        waiter.find_element(self.browser, "/html/body/div[4]/div/div[1]/div/div[2]/button", by=XPATH).click()

    def scrape_followings(self, user: User):
        try:
            upper_buttons = self.browser.find_elements_by_class_name('-nal3 ')
            upper_buttons[2].click()
            waiter.find_element(self.browser, "//div[@role='dialog']", by=XPATH)
        except Exception as e:
            print(user.username, ' does not have followings')
            return
        followings = []
        following_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
        time.sleep(1.5 + random.random() * 2)
        if int(user.following_count) > 0:
            for following_index in range(1, int(user.following_count) + 1):
                try:
                    following_index = str(following_index)
                    followings.append(waiter.find_element(self.browser, following_css.format(following_index)).text)
                    if following_index == user.following_count:
                        break
                    if int(following_index) % 4 == 0:
                        last_follower = waiter.find_element(self.browser, following_css.format(following_index))
                        self.browser.execute_script("arguments[0].scrollIntoView();", last_follower)
                        time.sleep(0.45 + random.random()*0.1)
                except Exception as e:
                    print(e)
                    break
        print('\tFollowings -', user.following_count, 'scrapped: ', len(followings))
        user.followings = followings

    def scrape_base(self, username):
        user = User(username)
        for i in range(3):
            try:
                self.browser.get(f'https://www.instagram.com/{username}/')
                time.sleep(WAITING_TIME + 4)
                upper_labels = self.browser.find_elements_by_class_name('-nal3 ')
                if len(upper_labels) >= 3:
                    break
            except Exception as e:
                pass
        else:
            raise AccountDoesNotExist(f'User {user.username} does not exist')

        user.media_count = upper_labels[0].text.split()[0] if len(upper_labels[0].text.split()) == 2 else ''.join(upper_labels[0].text.split()[:2])
        user.follower_count = upper_labels[1].text.split()[0] if len(upper_labels[1].text.split()) == 2 else ''.join(upper_labels[1].text.split()[:2])
        user.following_count = upper_labels[2].text.split()[0] if len(upper_labels[2].text.split()) == 2 else ''.join(upper_labels[2].text.split()[:2])

        if 'тыс.' in user.media_count:
            user.media_count = str(int(float(user.media_count.replace('тыс.', '').replace(',', r'.')) * 1000))
        elif 'млн' in user.media_count:
            user.media_count = str(int(float(user.media_count.replace('млн', '').replace(',', r'.')) * 1000000))

        if 'тыс.' in user.follower_count:
            user.follower_count = str(int(float(user.follower_count.replace('тыс.', '').replace(',', r'.')) * 1000))
        elif 'млн' in user.follower_count:
            user.follower_count = str(int(float(user.follower_count.replace('млн', '').replace(',', r'.')) * 1000000))

        if 'тыс.' in user.following_count:
            user.following_count = int(float(user.following_count.replace('тыс.', '').replace(',', r'.')) * 1000)
        if 'млн' in user.following_count:
            user.following_count = int(float(user.following_count.replace('млн', '').replace(',', r'.')) * 1000000)

        try:
            private_label = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div/div')
            if private_label.text != '':
                user.isPrivate = True
        except selenium.common.exceptions.NoSuchElementException:
            pass
        name_label = self.browser.find_element_by_class_name('-vDIg')
        text = name_label.text.split('\n')
        if len(text) > 0:
            user.name = text[0]
        if len(text) > 1:
            user.biography = ','.join(text[1:])
        return user


if __name__ == '__main__':
    insta_username = input('Enter Instagram username:')
    insta_password = input('Enter Instagram password')
    postgres_username = input('Enter postgres username')
    postgres_password = input('Enter postgres password')
    # CONNECT TO POSTGRES DB
    con = psycopg2.connect(
        database="postgres",
        user=postgres_username,
        password=postgres_password,
        host="127.0.0.1",
        port="5432")
    cur = con.cursor()
    visited_db = 'usernames_visited_1'
    queue_db = 'usernames_queue_1'
    data_db = 'data_1'

    bot = InstagramBot(insta_username, insta_password)
    bot.signIn()
    count = 0
    exception_counter = 0
    while True:
        if exception_counter > 2:
            raise Exception('We are probably banned :(')
        count += 1
        current_username = select(cur, queue_db)[0][0] if select(cur, queue_db) else 'ilya_fisher_volga'
        print(current_username)
        try:
            current_user = bot.scrape_user(current_username)
            for follower in current_user.followers:
                follower = follower.replace("\'", ' ')
                if not isInDatabase(cur, follower, visited_db) and not isInDatabase(cur, follower, queue_db):
                    insert(cur, con, follower, queue_db)
            for follower in current_user.followings:
                follower = follower.replace("\'", ' ')
                if not isInDatabase(cur, follower, visited_db) and not isInDatabase(cur, follower, queue_db):
                    insert(cur, con, follower, queue_db)
            current_user.username = current_user.username.replace('\'', ' ')
            current_user.name = current_user.name.replace('\'', ' ')
            current_user.biography = current_user.biography.replace('\'', ' ')
            current_user.joined_followers = ','.join(current_user.followers)
            current_user.joined_followings = ','.join(current_user.followings)
            drop(cur, con, current_username, queue_db)
            if not isInDatabase(cur, current_username, visited_db):
                insert(cur, con, current_username, visited_db)
                insert_data(cur, con, data_db, current_user)
                time.sleep(2 + random.random() * 4)
        except AccountDoesNotExist as e:
            drop(cur, con, current_username, queue_db)
            exception_counter += 1
            print(e)


