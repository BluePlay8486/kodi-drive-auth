import requests

class GoogleOAuth:
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"

    SCOPES = (
        "https://www.googleapis.com/auth/drive "
        "https://www.googleapis.com/auth/drive.file "
        "https://www.googleapis.com/auth/userinfo.profile"
    )

    @staticmethod
    def build_auth_url(client_id, redirect_uri):
        import urllib.parse

        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": GoogleOAuth.SCOPES,
            "access_type": "offline",
            "prompt": "consent"
        }

        return f"{GoogleOAuth.AUTH_URL}?{urllib.parse.urlencode(params)}"

    @staticmethod
    def exchange_code_for_tokens(client_id, client_secret, redirect_uri, code):
        data = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        r = requests.post(GoogleOAuth.TOKEN_URL, data=data)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def refresh_token(client_id, client_secret, refresh_token):
        data = {
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
        }

        r = requests.post(GoogleOAuth.TOKEN_URL, data=data)
        r.raise_for_status()
        return r.json()
