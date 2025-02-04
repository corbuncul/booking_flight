from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import config

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
INFO = {
    'type': config.google.type,
    'project_id': config.google.project_id,
    'private_key_id': config.google.private_key_id,
    'private_key': config.google.private_key.get_secret_value(),
    'client_email': config.google.client_email,
    'client_id': config.google.client_id,
    'auth_uri': config.google.auth_uri,
    'token_uri': config.google.token_uri,
    'auth_provider_x509_cert_url': config.google.auth_provider_x509_cert_url,
    'client_x509_cert_url': config.google.client_x509_cert_url,
}

cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
