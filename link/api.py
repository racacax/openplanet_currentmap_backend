import base64

import requests
from django.urls import reverse

from currentmap.settings import TRACKMANIA_API_BASE_URL, TRACKMANIA_APP_ID, TRACKMANIA_APP_CLIENT_SECRET, \
    MANIAPLANET_API_BASE_URL, MANIAPLANET_APP_CLIENT_SECRET, MANIAPLANET_APP_ID


class Trackmania2020API(object):
    def __init__(self, code, request):
        self.code = code
        self.request = request
        self.token = None

    def get_token(self):
        if not self.token:
            r = requests.post(f"{TRACKMANIA_API_BASE_URL}api/access_token",
                              data={"grant_type": "authorization_code",
                                    "client_secret": TRACKMANIA_APP_CLIENT_SECRET,
                                    "client_id": TRACKMANIA_APP_ID,
                                    "redirect_uri": self.request.build_absolute_uri(reverse('reset_2020')),
                                    "code": self.code},
                              headers={'Accept': 'application/json'})
            result = r.json()
            if "access_token" in result:
                self.token = result["access_token"]
        return self.token

    def get_user_data(self):
        r = requests.get(f"{TRACKMANIA_API_BASE_URL}api/user",
                         headers={'Accept': 'application/json', 'Authorization': f'Bearer {self.get_token()}'})
        result = r.json()
        if "account_id" in result:
            result["login"] = self.get_login_from_account_id(result["account_id"])
        return result

    """
    Adapted from Beu PHP Script
    """
    @staticmethod
    def get_login_from_account_id(account_id: str):
        account_id = account_id.replace("-", "")
        login = ""
        for pair in [account_id[i:i+2] for i in range(0, len(account_id), 2)]:
            login += chr(int(int(pair, 16)))
        login = base64.b64encode(login.encode('latin-1')).decode("utf-8")
        login = login.replace("+", "-").replace("/", "_").replace("=", "")
        return login


class ManiaPlanet4API(object):
    def __init__(self, code, request):
        self.code = code
        self.request = request
        self.token = None

    def get_token(self):
        if not self.token:
            r = requests.post(f"{MANIAPLANET_API_BASE_URL}login/oauth2/access_token",
                              data={"grant_type": "authorization_code",
                                    "client_secret": MANIAPLANET_APP_CLIENT_SECRET,
                                    "client_id": MANIAPLANET_APP_ID,
                                    "redirect_uri": self.request.build_absolute_uri(reverse('reset_mp4')),
                                    "code": self.code},
                              headers={'Accept': 'application/json'})
            result = r.json()
            if "access_token" in result:
                self.token = result["access_token"]
        return self.token

    def get_user_data(self):
        r = requests.get(f"{MANIAPLANET_API_BASE_URL}webservices/me",
                         headers={'Accept': 'application/json', 'Authorization': f'Bearer {self.get_token()}'})
        result = r.json()
        return result
