import os
from pathlib import Path
import requests
import json
import getpass

config_file = os.path.join(Path.home(), "pandahub.config")

def login():
    url = input("Enter pandahub URL: ")
    cert_path = None
    key_path = None

    # ask for client certificates
    while(True):
        with_client_ssl = input("Certificate for API needed? (y/n): ")
        if with_client_ssl != "y" and with_client_ssl != "n":
            print("ERROR: Wrong input! Only 'y' or 'n' are accepted!")
        else:
            if with_client_ssl == "y":
                cert_path = input("Path to client certificate (*.crt): ")
                key_path = input("Path to client key (*.key): ")
            break

    email = input("Enter E-Mail: ")
    password = getpass.getpass("Enter Password: ")
    _login(url, email, password, cert_path, key_path)

def _login(url, email, password, cert_path=None, key_path=None):
    print("Logging into pandbase at {}".format(url))
    print("pandahub API URL {}".format(url))
    path = url + "/auth/login"

    cert = None
    if cert_path and key_path:
        cert = (cert_path, key_path)

    r = requests.post(path, data={"username": email, "password": password}, cert=cert)

    if r.status_code == 200:
        token = r.json()["access_token"]
        print("Writing access token to config file...")
        write_config(url, token, cert_path, key_path)
        print("Login succesfull.")
    elif r.status_code == 400:
        if "required SSL certificate" in r.text:
            print("Login failed - no client certificate provided")
        else:
            print("Login failed - bad credentials.")
    else:
        print(f"[ERROR] code: {r.status_code}, reason: {r.reason}")

def write_config(url, token, cert_path="", key_path=""):
    with open(config_file, "w") as f:
        json.dump({
            "url": url,
            "token": token,
            "client_cert_path": cert_path,
            "client_key_path": key_path
        }, f)

if __name__ == '__main__':
    url='127.0.0.1'
    email = "leon.thurner2@retoflow.de"
    password = "mypass"
    _login(url, email, password)
