#!/usr/bin/env -S /usr/bin/python -Wall -Wignore::DeprecationWarning
"""
Detect webauthn users without phones
"""

import os
import smtplib
import sys
import csv
import duo_client
import configparser

import argparse
import pprint

def process_arguments():

    parser = argparse.ArgumentParser(
        description="""
            Automatically clean up phones in the limbo state of "Generic Smartphone" 
            in Duo Security.""",
    )

    parser.add_argument(
        '--duo-credentials-file',
        type=os.path.expanduser,
        help="""path to credentials.ini . Default:\n
            ~/.config/IAS/ias-duo-phone-cleanup/credentials.ini""",
        default='~/.config/IAS/ias-duo-phone-cleanup/credentials.ini'
    )

    parser.add_argument(
        '--dump-config',
        help="Prints the config and arguments to stdout.",
        action='store_true'
    )

    args = parser.parse_args()

    return args

def get_users(admin_api):
    try:
        return admin_api.get_users()
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def detect_webauthn_without_phone(user):
    try:
        user_id = user['user_id']
        phones = user['phones']
        if len(user['webauthncredentials']) > 0 and len(user['phones']) == 0:
            print(f"User: {user['username']} WebAuthN: {user['webauthncredentials']}")

    except Exception as e:
        print(f"Error: {str(e)}")

def do_work():

    args = process_arguments()
    config = configparser.ConfigParser()
    config.read(args.duo_credentials_file)


    if (args.dump_config):
        print("Arguments:")
        pprint.pp(args)
        print("Config:")
        print({section: dict(config[section]) for section in config})

    # Configuration and information about objects to create.
    admin_api = duo_client.Admin(
        ikey=config['duo']['ikey'],
        skey=config['duo']['skey'],
        host=config['duo']['host'],
    )

    # Retrieve user info from API:
    users = get_users(admin_api)
    for user in users:
        detect_webauthn_without_phone(user)

if __name__ == "__main__":
    do_work()
