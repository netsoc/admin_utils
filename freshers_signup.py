#!/usr/bin/env python3
import datetime
import json
import os
import time

import signal

# attempt to ignore ctrl-z
signal.signal(signal.SIGTSTP, signal.SIG_IGN)


def blinking(string):
	return '\33[5m' + string + '\33[0m'


BANNER = """ W e l c o m e   t o
   ______        __
  / ____ \ ___  / /__________  _____
 / / __ `// _ \/ __/ ___/ __ \/ ___/
/ / / / //  __/ /_(__  ) /_/ / /__
\/_/ /_/ \___/\__/____/\____/\___/
 \____/
           F r e s h e r s '  2 0 1 7
"""

def yes_no(prompt):
    answers = {
            'yes': True, 'y': True,
            'no': False, 'n': False
            }
    text = ''
    print(prompt)
    while not text.lower() in answers:
        text = input(' [y/n] >> ')
    return answers[text.lower()]


def get_email(prompt):
    text = input(prompt)
    while '@' not in text:
        print(' An email address typically has an `@` in it...')
        text = input('       >> ')
    return text


def get_username(prompt):
    while True:
        username = input(prompt)
        if username == "":
            break

        confirmed = input(" And again, just to confirm.\n       >> ")

        if (confirmed != username):
            print("       Entries do not match!\n")
        else:
            break
    return username


def get_name(prompt):
    while True:
        name = input(prompt)
        if not name:
            print("  We need something, anything!")
        elif name.lower() in ['hugh mungus', 'hugh mongus']:
            print(blinking("  Now that's one SPICY MEME"))
        else:
            return name


def get_user_details():
    user = dict()
    prompts = (
            ("What's your name?\n"
             "       >> ",
             'name',
             get_name),

            ("What's your email address?\n"
             "       >> ",
             'email',
             get_email),

            ("Are you already a member?",
             'renewing',
             yes_no),

            ("What's your username? "
             " (if you remember it, leave blank if you don't!)"
             "\n       >> ",
             'username',
             get_username),

            ("Want to subscribe to our jobs & internships mailing list?",
             'jobseeker',
             yes_no),
    )

    for prompt_text, key, input_func in prompts:
        if key == 'username' and not user['renewing']:
            continue
        response = input_func(prompt_text)
        if key != 'username' or response != "":
            user[key] = response
    return user


def fmt_details(user):
    l = 60
    details = ('           Name: {name}\n'
               '  Email address: {email}'
               .format(name=user['name'], email=user['email']))

    if 'username' in user:
        username = ('\n       Username: {username}'
                    .format(username=user['username']))
    else:
        username = ''

    jobseeker_text = ("  You{}want to receive job & internship emails"
                      .format(' ' if user['jobseeker'] else " don't "))

    renewing_text = ("  You are renewing your membership\n" if user['renewing']
                     else "  You are not already a member\n")

    return ("So, to confirm:\n\n" +
            ("#" * l) + '\n' +
            details +
            username + '\n\n' +
            jobseeker_text + '\n' +
            renewing_text +
            ("#" * l) + '\n')


def register_user(users_file, user):
    with open(users_file, 'r') as f:
        users = json.load(f)
        users.append(user)
    with open(users_file, 'w') as f:
        json.dump(users, f)


def prep_screen():
    os.system('clear')
    print(BANNER)


def signups(users_file):
    while True:
        try:
            prep_screen()
            user = get_user_details()
            print('\n')
            print(fmt_details(user))
            valid = yes_no("Are **all** of these details correct?")
            if valid:
                register_user(users_file, user)
                print("Welcome, {}!".format(user['name'].split(' ')[0]))
                time.sleep(2)
                for _ in range(25):
                    print()
                    time.sleep(0.05)
            else:
                continue
        except (KeyboardInterrupt, EOFError):
            try:
                kill = input('<')
                if kill == 'kill':
                    break
            except (KeyboardInterrupt, EOFError):
                continue
            continue


def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = "freshers_{}.json".format(timestamp)
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            json.dump([], f)
    signups(filename)


if __name__ == '__main__':
    main()
