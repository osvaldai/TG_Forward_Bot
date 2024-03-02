import os
import re

from telethon import TelegramClient, events

api_id = 1137549
api_hash = '6a3dc4e051465fc0266835b6f4dd6777'

client_tg = TelegramClient('session_name_forward.session', api_id, api_hash)

chat = -1001322515232  # Например, -1001322515232
destination_chat = os.environ.get("chat_id_target")  # ID целевого чата, куда будет пересылаться сообщение


def extract_trading_info(message):
    """
    Extracts trading information from a given message string.

    :param message: A string containing trading signal information.
    :return: A dictionary with extracted trading pair, entry price range, stop loss, and target prices.
    """
    # Regular expressions to match trading info patterns
    pair_pattern = r'COIN:\s*\$(\w+/\w+)'
    entry_pattern = r'ENTRY:\s*([0-9.]+)\s*-\s*([0-9.]+)'
    stop_loss_pattern = r'STOP LOSS:\s*([0-9.]+)'
    targets_pattern = r'TARGETS.*?Mid Term:\s*([0-9. -]+)'

    # Extract information using regular expressions
    trading_pair = re.search(pair_pattern, message)
    entry_price = re.search(entry_pattern, message)
    stop_loss = re.search(stop_loss_pattern, message)
    targets = re.search(targets_pattern, message, re.DOTALL)

    # Extracting and formatting target prices
    if targets:
        targets = [float(price.strip()) for price in targets.group(1).split('-')]

    # Creating the result dictionary
    result = {
        'trading_pair': trading_pair.group(1) if trading_pair else None,
        'entry_price_range': (float(entry_price.group(1)), float(entry_price.group(2))) if entry_price else None,
        'stop_loss': float(stop_loss.group(1)) if stop_loss else None,
        'targets': targets
    }

    return result


def is_similar_to_signal(message):
    # Разбиваем сообщение на строки
    lines = message.split('\n')

    # Проверяем каждую строку
    for line in lines:
        if re.search(r'📍SIGNAL\sID:\s#\d+📍', line):
            continue
        elif re.search(r'COIN:\s\$\w+/\w+', line):
            continue
        elif re.search(r'Direction:\s\w+📈?', line):
            continue
        elif re.search(r'ENTRY:\s[\d\.\s\-]+', line):
            continue
        elif 'TARGETS' in line:
            continue
        elif re.search(r'STOP\sLOSS:\s[\d\.]+', line):
            return True  # Возвращаем True, если все проверки пройдены и найдена последняя строка

    return False  # Возвращаем False, если какая-то проверка не пройдена


@client_tg.on(events.NewMessage(chats=chat))
async def normal_handler_1(event):
    txt = str(event.message.to_dict()['message']).replace('- Binance Killers®', '').replace(
        'This message cannot be forwarded or replicated', '')
    # message = event.message
    if is_similar_to_signal(txt):
        # if message.media:  # Проверяем, есть ли медиа в сообщении
        #     await client_tg.send_file(
        #         entity=destination_chat,
        #         file=message.media,
        #         caption=txt  # Текст сообщения в качестве подписи к медиа
        #     )
        #     print('Forwarded message with media')
        # else:
        # Если медиа нет, просто пересылаем текст
        await client_tg.send_message(
            entity=destination_chat,
            message=txt
        )
        print('Forwarded text message')


client_tg.start()
client_tg.run_until_disconnected()
