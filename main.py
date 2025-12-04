from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from google_oauth import GoogleOAuth
from utils import error

app = FastAPI()


# -------------------------------------------------------------------
# 0) ROTA OBRIGATÓRIA — CloudDrive SEMPRE chama esta primeiro
# -------------------------------------------------------------------
@app.get("/ip")
async def get_ip(request: Request):
    client_ip = request.client.host
    return {"ip": client_ip}


# -------------------------------------------------------------------
# 1) ROTA PRINCIPAL — CloudDrive usa ESTA para gerar a URL de login
# -------------------------------------------------------------------
@app.get("/pin")
async def pin(client_id: str, redirect_uri: str):
    """
    CloudDrive chama isto para obter a URL de autorização.
    """
    url = GoogleOAuth.build_auth_url(client_id, redirect_uri)

    return {
        "pin": "",
        "password": "",
        "verification_url": url
    }


# -------------------------------------------------------------------
# 2) Alternativa opcional (criadores antigos usavam create_pin)
# -------------------------------------------------------------------
@app.get("/create_pin")
async def create_pin(client_id: str, redirect_uri: str):
    url = GoogleOAuth.build_auth_url(client_id, redirect_uri)
    return {
        "pin": "",
        "password": "",
        "verification_url": url
    }


# -------------------------------------------------------------------
# 3) EXCHANGE CODE → TOKENS
# -------------------------------------------------------------------
@app.post("/token")
async def get_tokens(request: Request):

    data = await request.json()

    # Required fields
    required = ["client_id", "client_secret", "redirect_uri", "code"]
    for field in required:
        if field not in data:
            return error(f"Missing field: {field}")

    # CloudDrive está mandando code = "" → precisamos validar
    if not data["code"]:
        return error("Invalid authorization code (empty). Did you approve access?")

    try:
        tokens = GoogleOAuth.exchange_code_for_tokens(
            data["client_id"],
            data["client_secret"],
            data["redirect_uri"],
            data["code"]
        )
    except Exception as e:
        return error(f"Token exchange failed: {str(e)}")

    return tokens


# -------------------------------------------------------------------
# 4) REFRESH TOKEN
# -------------------------------------------------------------------
@app.post("/refresh")
async def refresh_tokens(request: Request):

    data = await request.json()

    required = ["client_id", "client_secret", "refresh_token"]
    for field in required:
        if field not in data:
            return error(f"Missing field: {field}")

    try:
        new_tokens = GoogleOAuth.refresh_token(
            data["client_id"],
            data["client_secret"],
            data["refresh_token"]
        )
    except Exception as e:
        return error(f"Refresh failed: {str(e)}")

    return new_tokens
