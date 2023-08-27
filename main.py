import asyncio
import click
import os
import json
import requests
from bs4 import BeautifulSoup
from time import sleep
from colorama import Fore
import colorama
import yaml


import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
from googlesamples.assistant.grpc import browser_helpers
from googlesamples.assistant.grpc.textinput import SampleTextAssistant


class DeviceUnavailableException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_config():
    with open('config.yml') as config:
        return yaml.load(config, Loader=yaml.Loader)


# this method has been adapted from googlesamples.assistant.grpc.textinput
async def query_assistant(query):
    api_endpoint = 'embeddedassistant.googleapis.com'
    credentials = os.path.join(click.get_app_dir('google-oauthlib-tool'), 'credentials.json')
    project_id = get_config()['project_id']
    model_id = get_config()['model_id']
    lang = 'en-US'
    display = True
    grpc_deadline = 60 * 3 + 5

    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        print(f'Error loading credentials: {e}')
        print('Run google-oauthlib-tool to initialize new OAuth 2.0 credentials.')
        return

    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)

    with SampleTextAssistant(lang, model_id, project_id, display,
                             grpc_channel, grpc_deadline) as assistant:
        print(f'{Fore.BLUE}Client: {query}')
        response_html = assistant.assist(text_query=query)[1]
        if display and response_html:
            system_browser = browser_helpers.system_browser
            # system_browser.display(response_html)

            soup = BeautifulSoup(response_html, features='html.parser')
            response_text = soup.select('.show_text_content')[0].text
            print(f'{Fore.RED}Server: {response_text}')
            return response_text


async def get_temperatures():
    response_text = await query_assistant('what is the ac temperature')

    if 'sorry' in response_text.lower():
        print(f'Error requesting ac temperature: {response_text}')
        raise DeviceUnavailableException(response_text)

    temperatures = [int(part) for part in response_text.split(' ') if part.isdigit()]
    if len(temperatures) == 2:
        ac_temp, house_temp = temperatures
    else:
        ac_temp = temperatures[0]
        house_temp = temperatures[0]
    return ac_temp, house_temp


async def get_fan_speed():
    response_text = await query_assistant('what is tim fan speed')

    if 'sorry' in response_text.lower():
        print(f'Error requesting fan speed: {response_text}')
        raise DeviceUnavailableException(response_text)

    fan_speeds = {
        'isn\'t running': {
            'speed': 0,
            'action': 'Turned fan off'
        },
        'slow': {
            'speed': 1,
            'action': 'Set fan speed to slow'
        },
        'medium': {
            'speed': 2,
            'action': 'Set fan speed to medium'
        },
        'fastest': {
            'speed': 4,
            'action': 'Set fan speed to fast'
        },
        'fast': {
            'speed': 3,
            'action': 'Set fan speed to fastest'
        }
    }
    fan_speed = None
    for phrase, test_fan_speed in fan_speeds.items():
        if phrase in response_text.lower():
            fan_speed = test_fan_speed
            break
    if fan_speed is None:
        raise Exception(f'Error finding fan speed: {response_text}')
    return fan_speed


async def set_fan_speed(fan_speed):
    fan_speeds = {
        0: {
            'query': 'turn tim fan off',
            'action': 'Turned fan off'
        },
        1: {
            'query': 'set tim fan speed to slow',
            'action': 'Set fan speed to slow'
        },
        2: {
            'query': 'set tim fan speed to medium',
            'action': 'Set fan speed to medium'
        },
        3: {
            'query': 'set tim fan speed to fast',
            'action': 'Set fan speed to fast'
        },
        4: {
            'query': 'set tim fan speed to fastest',
            'action': 'Set fan speed to fastest'
        },
    }
    fan_speed_lang = fan_speeds[fan_speed]
    response_text = await query_assistant(fan_speed_lang['query'])

    if 'sorry' in response_text.lower():
        print(f'Error requesting fan speed: {response_text}')
        raise DeviceUnavailableException(response_text)

    return fan_speed_lang


def send_push_notification(message):
    url = 'https://api.pushover.net/1/messages.json'
    data = {
        'token': get_config()['pushover_token'],
        'user': get_config()['pushover_user'],
        'message': message,
    }
    requests.post(url, json=data)


sim_house_temp = 55
sim_house_temp_change = -1
is_fan_disabled = False
last_fan_speed_lang = None


async def main():
    global sim_house_temp, sim_house_temp_change

    global is_fan_disabled, last_fan_speed_lang
    while True:
        ac_temp, house_temp = await get_temperatures()
        # sim_house_temp += change
        # if sim_house_temp <= 48:
        #     change = 1
        # ac_temp, house_temp = 50, sim_house_temp

        print(f'{Fore.LIGHTGREEN_EX}AC Temperature: {ac_temp} House Temperature: {house_temp}')
        if house_temp > ac_temp and not is_fan_disabled:
            is_fan_disabled = True
            last_fan_speed_lang = await get_fan_speed()
            if last_fan_speed_lang['speed'] != 0:
                await set_fan_speed(0)
                send_push_notification('Fan disabled bcause the AC turned on')
        elif house_temp <= ac_temp and is_fan_disabled:
            is_fan_disabled = False
            current_fan_speed_lang = await get_fan_speed()
            if current_fan_speed_lang['speed'] == 0:
                fan_speed_lang = await set_fan_speed(last_fan_speed_lang['speed'])
                send_push_notification(fan_speed_lang['action'])
        sleep(60)


colorama.init(autoreset=True)
send_push_notification('test')
# asyncio.run(main())
