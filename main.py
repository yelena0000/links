import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, link):

    api_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'access_token': token,
        'v': '5.199',
        'url': link
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        response_data = response.json()
        if 'error' in response_data:
            return f"Ошибка: {response_data['error']['error_msg']}"
        return response_data['response']['short_url']

    except requests.exceptions.RequestException as error:
        return f"Ошибка: {error}"


def count_clicks(token, short_link):

    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    key = urlparse(short_link).path.strip('/')
    params = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': '5.199',
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        response_data = response.json()
        if 'error' in response_data:
            return f"Ошибка: {response_data['error']['error_msg']}"
        if response_data['response']['stats'] == []:
            return 'нет статистики по количеству кликов'
        return response_data['response']['stats'][0]['views']

    except requests.exceptions.RequestException as error:
        return f"Ошибка: {error}"


def is_shorten_link(link):
    netloc = urlparse(link).netloc
    return netloc == 'vk.cc'


def main():
    load_dotenv()
    access_token = os.environ['ACCESS_TOKEN']

    url = input("Введите ссылку: ")
    short_link = shorten_link(access_token, url)

    if not is_shorten_link(url):
        print(f"Короткая ссылка: {short_link}")
    else:
        click_stats = count_clicks(access_token, url)
        print(f"Количество кликов: {click_stats}")


if __name__ == "__main__":
    main()
