import requests


def fetch_user(user_id: int) -> dict:
    """Call a remote API and return JSON."""
    resp = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    resp.raise_for_status()
    return resp.json()


def get_company_name(user_id: int) -> str:
    user = fetch_user(user_id)
    return user.get("company", {}).get("name", "")
