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
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_data = response.json()

    if 'error' in response_data:
        raise ValueError(
            f"Ошибка VK API: {response_data['error']['error_msg']}")

    return response_data['response']['short_url']


def count_clicks(token, short_link):

    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    key = urlparse(short_link).path.strip('/')
    params = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': '5.199',
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_data = response.json()

    if 'error' in response_data:
        raise ValueError(
            f"Ошибка VK API: {response_data['error']['error_msg']}")

    if not response_data['response']['stats']:
        raise ValueError('Нет статистики по количеству кликов')

    return response_data['response']['stats'][0]['views']


def is_shorten_link(token, link):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    key = urlparse(link).path.strip('/')
    params = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': '5.199',
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_data = response.json()

    return 'error' not in response_data


def main():
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']

    url = input("Введите ссылку: ")

    try:
        if not is_shorten_link(access_token, url):
            short_link = shorten_link(access_token, url)
            print(f"Короткая ссылка: {short_link}")
        else:
            click_stats = count_clicks(access_token, url)
            print(f"Количество кликов: {click_stats}")
    except ValueError as error:
        print(error)
    except Exception as error:
        print(f"Непредвиденная ошибка: {error}")


if __name__ == "__main__":
    main()
