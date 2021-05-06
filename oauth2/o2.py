import requests
import json
import subprocess
import sys


def o2(authorize_url: str, token_url: str, callback_url: str, client_id: str, client_secret: str):
    authorization_redirect_url = f"{authorize_url}response_type=code&client={client_id}&redirect_uri={callback_url}&scope=openid"





if __name__ == '__main__':
    pass
