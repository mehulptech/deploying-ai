import requests
from langchain_core.tools import tool


@tool
def get_joke() -> str:
    """
    Fetches a random joke from a public API and rephrases it.
    """

    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url, timeout=10)
    except Exception:
        return "I tried to get a joke but something went wrong."

    if response.status_code != 200:
        return "The joke server is having a bad day."

    data = response.json()

    setup = data.get("setup", "")
    punchline = data.get("punchline", "")

    return (
        f"Alright, here's something slightly entertaining:\n\n"
        f"{setup}\n"
        f"...wait for it...\n"
        f"{punchline}\n\n"
        f"You're welcome."
    )