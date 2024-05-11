from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import (
    HarmBlockThreshold,
    HarmCategory,
)
from app.settings.env import Env


def init_vertexai():
    credentials_json = Env.GOOGLE_APPLICATION_CREDENTIALS_JSON
    credentials = service_account.Credentials.from_service_account_info(
        credentials_json
    )
    vertexai.init(
        project=Env.VERTEXAI_PROJECT_ID,
        location=Env.VERTEXAI_PROJECT_LOCATION,
        credentials=credentials,
    )


safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}
