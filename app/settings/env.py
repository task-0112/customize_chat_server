import os
import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())


def _getenv(key: str):
    env = os.getenv(key)
    if env is None:
        return env

    # 空文字列の場合はNoneを返す
    if env.strip() == "":
        os.environ.pop(key)
        return None

    return env


class Env:
    # GPT関連
    OPENAI_API_KEY = _getenv("OPENAI_API_KEY")

    # VERTEXAI GEMINI関係
    GOOGLE_APPLICATION_CREDENTIALS_JSON = {
        "type": _getenv("GOOGLE_APPLICATION_TYPE"),
        "project_id": _getenv("VERTEXAI_PROJECT_ID"),
        "private_key_id": _getenv("GOOGLE_APPLICATION_PRIVATE_KEY_ID"),
        "private_key": _getenv("GOOGLE_APPLICATION_PRIVATE_KEY"),
        "client_email": _getenv("GOOGLE_APPLICATION_CLIENT_EMAIL"),
        "client_id": _getenv("GOOGLE_APPLICATION_CLIENT_ID"),
        "auth_uri": _getenv("GOOGLE_APPLICATION_AUTH_URL"),
        "token_uri": _getenv("GOOGLE_APPLICATION_TOKEN_URL"),
        "auth_provider_x509_cert_url": _getenv("GOOGLE_APPLICATION_AUTH_PROVIDER_URL"),
        "client_x509_cert_url": _getenv("GOOGLE_APPLICATION_CLIENT_CERT_URL"),
        "universe_domain": _getenv("GOOGLE_APPLICATION_UNIVERSE_DOMAIN"),
    }
    VERTEXAI_PROJECT_ID = _getenv("VERTEXAI_PROJECT_ID")
    VERTEXAI_PROJECT_LOCATION = _getenv("VERTEXAI_PROJECT_LOCATION")
