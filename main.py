import os
import requests
from dotenv import load_dotenv
from supabase import Client, create_client

# Config do Logger
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",)
logger = logging.getLogger(__name__)

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
ZAPI_INSTANCE_ID = os.environ["ZAPI_INSTANCE_ID"]
ZAPI_TOKEN = os.environ["ZAPI_TOKEN"]
ZAPI_CLIENT_TOKEN = os.environ["ZAPI_CLIENT_TOKEN"]

MAX_CONTACTS = 3


# Função para buscar contatos no Supabase
def get_contacts(supabase: Client) -> list[dict]:
    """Busca até MAX_CONTACTS contatos no Supabase."""
    logger.info("Buscando contatos no Supabase...")

    response = (
        supabase.table("contacts")
        .select("name, phone")
        .limit(MAX_CONTACTS)
        .execute()
    )

    contacts = response.data
    logger.info(f"{len(contacts)} contato(s) encontrado(s).")
    return contacts

# Função para enviar mensagem via Z-API
def send_message(phone: str, name: str) -> bool:
    # Envia mensagem via Z-API. Retorna True em caso de sucesso.
    url = (f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}" f"/token/{ZAPI_TOKEN}/send-text")
    headers = {"Content-Type": "application/json", "Client-Token": ZAPI_CLIENT_TOKEN,}
    payload = {"phone": phone, "message": f"Olá, {name} tudo bem com você?",}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        logger.info(f"Mensagem enviada para {name} ({phone})")
        return True
    except requests.exceptions.HTTPError as err:
        logger.error(f"Erro HTTP ao enviar para {name} ({phone}): {err}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Erro de conexão ao enviar para {name} ({phone}): {err}")

    return False


# Executa o script principal
def main() -> None:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    contacts = get_contacts(supabase)
    if not contacts:
        logger.warning("Nenhum contato encontrado. Encerrando.")
        return

    success_count = sum( send_message(contact["phone"], contact["name"]) for contact in contacts)

    logger.info(f"Envio concluído: {success_count}/{len(contacts)} mensagem(ns) enviada(s) com sucesso.")


if __name__ == "__main__":
    main()