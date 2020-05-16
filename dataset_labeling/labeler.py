import json
import logging
import os
from tkinter.messagebox import showinfo

from datetime import datetime
import time
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import font
from tkinter import messagebox


URL = 'https://www.instagram.com/'
DATA_FILENAME = 'data/usernames.txt'
LABELS_FILENAME = 'results/labels.json'
NORMAL_USER = 'NORMAL'
MEDIA_USER = 'MEDIA'
BUSINESS_ACCOUNT = 'BUSINESS'
SPAMMER = 'SPAMMER'


class InstagramAgent:
    def __init__(self, email, password):
        self.browser = webdriver.Chrome('chromedriver.exe')
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

    def open_profile(self, username):
        self.browser.get(URL + f'{username}/')


def wrapper(start_window, username, password):
    if username.get() and password.get():
        start_window.destroy()
    else:
        messagebox.showerror("Error", "Username and password cannot be empty")


def enter_credentials():
    start_window = Tk()
    username = StringVar()
    password = StringVar()

    start_window.title('Enter you Instagram credentials')
    start_window.geometry('500x130+600+400')

    username_entry = Entry(start_window, textvariable=username, font=12)
    username_entry.place(relheight=0.25, relwidth=0.48, relx=0.5)
    password_entry = Entry(start_window, textvariable=password, font=12)
    password_entry.place(relheight=0.25, relwidth=0.48, rely=0.3, relx=0.5)

    label_username = Label(start_window, text='Enter Instagram username')
    label_username.place(relheight=0.2, relwidth=0.3)
    label_password = Label(start_window, text='Enter Instagram password')
    label_password.place(relheight=0.2, relwidth=0.3, rely=0.3)
    btn_create = Button(start_window, text='Ok',
                        command=lambda: wrapper(start_window, username, password))
    btn_create.place(relheight=0.25, relwidth=0.5, relx=0.25, rely=0.7)
    start_window.mainloop()
    return username, password


def main():
    Path('logs').mkdir(exist_ok=True)
    logging.basicConfig(filename='logs/labeler.log', level=logging.INFO,
                        format='%(asctime)s ---- %(message)s', datefmt='%Y.%m.%d_%H:%M:%S')
    logging.info('-----'*5 + ' New session ' + '-----'*5)
    try:
        Path('results').mkdir(exist_ok=True)
        if Path(LABELS_FILENAME).exists():
            with open(LABELS_FILENAME) as file:
                labels = json.load(file)
                with open(f'results/{datetime.today().strftime("%Y_%m_%d_%H_%M_%S")}.json',  'w') as dump_file:
                    json.dump(labels, dump_file, indent=4)
        else:
            with open(LABELS_FILENAME, 'w+') as file:
                labels = {}
                json.dump(labels, file, indent=4)
                pass
    except Exception as e:
        logging.exception(e)
        sys.exit(1)

    try:
        username, password = enter_credentials()
        root = Tk()
        root.withdraw()
        with open(DATA_FILENAME) as file:
            all_usernames = [line.rstrip('\n') for line in file]

        usernames = [user for user in all_usernames if user not in labels.keys()]
        if not usernames:
            showinfo(title="All users from usernames.txt are labeled", message="You can close the app")
            raise Exception('No more users')
        root.destroy()

        root = Tk()
        root.title('Instagram data labeling app')
        root.geometry('500x400+700+500')
        root['background'] = 'azure'

        username = username.get()
        password = password.get()
        index = [0]
        agent = InstagramAgent(username, password)
        agent.signIn()
        agent.open_profile(usernames[index[0]])
        current_user = StringVar()
        current_user.set(usernames[index[0]])

        main_font = font.Font(size=14)
        text_label = Label(root, text='Current username:', font=main_font)
        text_label.place(relheight=0.1, relwidth=0.6, relx=0.03, rely=0.2)
        user_label = Label(root, textvariable=current_user, font=main_font)
        user_label.place(relheight=0.1, relwidth=0.6, relx=0.03, rely=0.3)

        normal_button = Button(root, text='Normal user',
                             command=lambda: label_user(current_user, labels, NORMAL_USER, index, usernames, agent))
        normal_button.place(relheight=0.1, relwidth=0.3, relx=0.65, rely=0.2)

        spammer_button = Button(root, text='Potential spammer',
                             command=lambda: label_user(current_user, labels, SPAMMER, index, usernames, agent))
        spammer_button.place(relheight=0.1, relwidth=0.3, relx=0.65, rely=0.35)

        media_button = Button(root, text='Media person',
                             command=lambda: label_user(current_user, labels, MEDIA_USER, index, usernames, agent))
        media_button.place(relheight=0.1, relwidth=0.3, relx=0.65, rely=0.5)

        business_button = Button(root, text='Business account',
                             command=lambda: label_user(current_user, labels, BUSINESS_ACCOUNT, index, usernames, agent))
        business_button.place(relheight=0.1, relwidth=0.3, relx=0.65, rely=0.65)

        root.mainloop()
    except Exception as e:
        logging.exception(e)
    finally:
        with open(LABELS_FILENAME, 'w') as file:
            json.dump(labels, file, indent=4)


def label_user(current_user: StringVar, labels: dict, label: str, index: list, usernames: list, agent: InstagramAgent):

    if current_user.get() not in labels.keys():
        labels[current_user.get()] = label
        if current_user.get() in labels:
            if index[0] + 1 < len(usernames):
                index[0] += 1
                current_user.set(usernames[index[0]])
                agent.open_profile(usernames[index[0]])
            else:
                messagebox.showinfo("No more users :)", "You can close the app")
        else:
            messagebox.showerror("This user was not labeled", "Please classify him")


def next_user(index: list, current_user: StringVar, usernames: list, agent: InstagramAgent, labels: dict):
    if current_user.get() in labels:
        if index[0] + 1 < len(usernames):
            index[0] += 1
            current_user.set(usernames[index[0]])
            agent.open_profile(usernames[index[0]])
        else:
            messagebox.showinfo("No more users :)", "You can close the app")
    else:
        messagebox.showerror("This user was not labeled", "Please classify him")


if __name__ == '__main__':
    main()
