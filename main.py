from time import sleep

import telegram

from atm import atm_sorted_with_distance

MY_LAT, MY_LNG = 55.753410, 37.618450
TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = 123456

SLEEP_TIME = 60


def format_message(sorted_atm):
    message = ""
    for num, atm in enumerate(sorted_atm):
        atm_data, atm_distance = atm
        atm_distance = round(atm_distance)
        atm_address = atm_data["address"]

        atm_location = atm_data['location']
        atm_lat = atm_location['lat']
        atm_lng = atm_location['lng']
        yandex_link = f'https://yandex.ru/maps/?text={atm_lat},{atm_lng}'
        atm_distance_link = f'[{atm_distance} м]({yandex_link})'

        message += f'{num+1}. {atm_address} - {atm_distance_link}\n'
    return message


def main_loop(bot):
    last_state = []

    while True:
        sorted_atm = atm_sorted_with_distance(MY_LAT, MY_LNG)
        if last_state == sorted_atm:
            print("Same state. Waiting...")
            sleep(SLEEP_TIME)
            continue

        last_state = sorted_atm
        message = format_message(sorted_atm)
        print("Sending new state...")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

        print("Waiting...")
        sleep(SLEEP_TIME)


def main():
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Стартую проверки банкоматов!")

    try:
        main_loop(bot)
    except Exception as e:
        message = f"Всё сломалось:\n{e}"
        print(message)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        raise


if __name__ == '__main__':
    main()
