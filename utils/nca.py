import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def verify_ecp_signature(signed_data: str, nonce: str) -> tuple[str, str]:
    response = requests.post(
        settings.NCANODE_URL,
        json={
            "cms": signed_data,
            "revocationCheck": ["OCSP"],
            "data": nonce
        },
        auth=HTTPBasicAuth(settings.NCANODE_BASIC_USER, settings.NCANODE_BASIC_PASS),
        timeout=10,
    )
    response.raise_for_status()
    result = response.json()

    if not result.get("valid"):
        raise Exception("Подпись недействительна")

    subject = result["signers"][0]["certificates"][0]["subject"]
    iin = subject.get("iin")
    name = subject.get("commonName")


    if not iin or not name:
        raise Exception("Невозможно извлечь IIN или ФИО из сертификата")

    return iin, name
