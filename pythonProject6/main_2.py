import requests
import json


baseURL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
if __name__ == "__main__":
    response = requests.get(f"{baseURL}")
    print(response)