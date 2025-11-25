import requests
import json
from datetime import datetime, timedelta
import time
import pytz

BASE_URL = "https://dados.mobilidade.rio/gps/sppo"

RIO_TZ = pytz.timezone('America/Sao_Paulo')

def fetch_and_save_data():
    try:
        end_time = datetime.now(RIO_TZ)
        start_time = end_time - timedelta(hours=1)

        formatted_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        url = f"{BASE_URL}?dataInicial={formatted_start_time}&dataFinal={formatted_end_time}"

        print(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] Requesting data from: {url}")

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        filename_timestamp = end_time.strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"/root/sppo/sppo_data_{filename_timestamp}.json"

        # Save the data to the file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Successfully downloaded data and saved to {filename}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
