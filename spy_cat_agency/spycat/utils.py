import requests

def is_valid_breed(breed):
    response = requests.get("https://api.thecatapi.com/v1/breeds")
    if response.status_code == 200:
        breeds = [b["name"] for b in response.json()]
        return breed in breeds
    return False
