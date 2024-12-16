import os
import re
from time import sleep

from telethon import TelegramClient, events

from trade_info_extractor import parse_trade_message, is_trade_message, parse_trade_message_49, \
    is_valid_trade_message_49, parse_trading_signal, is_valid_trading_summary, parse_trade_message_final, \
    is_trading_signal, clean_message

api_id = 
api_hash = ''

client_tg = TelegramClient('session_name_forward.session', api_id, api_hash)

chat = 0  # Например, -
destination_chat = 0  # ID целевого чата, куда будет пересылаться сообщение


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


def is_similar_to_signal_TP(message):
    lines = message.split('\n')

    # Флаги для проверки каждого элемента
    has_signal_id, has_coin, has_direction, has_targets, has_profit, = False, False, False, False, False,

    for line in lines:
        if re.search(r'📍SIGNAL\sID:\s#\d+📍', line):
            has_signal_id = True
        elif re.search(r'COIN:\s\$\w+/\w+', line):
            has_coin = True
        elif re.search(r'Direction:\s\w+📈?', line):
            has_direction = True
        elif re.search(r'Target\s\d+:', line):
            has_targets = True
        elif re.search(r'🔥[\d\.]+% Profit', line):
            has_profit = True

    # Проверяем, что все элементы присутствуют
    return all([has_signal_id, has_coin, has_direction, has_targets, has_profit, ])


@client_tg.on(events.NewMessage(chats=-1001736278884))
async def normal_handler_1(event):
    """Bitcoin premium Channel 1001736278884"""
    txt = str(event.message.to_dict()['message']).replace('- Binance Killers®', '').replace(
        'This message cannot be forwarded or replicated', '')
    message = event.message
    if parse_trade_message(message)['trade_side'] is not None or is_trade_message(message):
        await client_tg.send_message(
            entity=destination_chat,
            message=txt
        )
    print('Forwarded text message')


@client_tg.on(events.NewMessage(chats=-1001525644349))
async def normal_handler_1(event):
    """rus fed premium channel 1001525644349"""
    txt = str(event.message.to_dict()['message']).replace('- Binance Killers®', '').replace(
        'This message cannot be forwarded or replicated', '').replace('Fed. Russian Insiders®', '')
    message = event.message
    if parse_trade_message_49(message) or is_valid_trade_message_49(message):
        await client_tg.send_message(
            entity=destination_chat,
            message=txt
        )
        print('Forwarded text message')


@client_tg.on(events.NewMessage(chats=0))
async def normal_handler_1(event):
    """"""
    txt = str(event.message.to_dict()['message']).replace('- Binance Killers®', '').replace(
        'This message cannot be forwarded or replicated', '')
    message = event.message
    if parse_trading_signal(message) or is_valid_trading_summary(message):
        await client_tg.send_message(
            entity=destination_chat,
            message=txt
        )
    print('Forwarded text message')


@client_tg.on(events.NewMessage(chats=0))
async def normal_handler_1(event):
    """"""
    txt = str(event.message.to_dict()['message']).replace('- Binance Killers®', '').replace(
        'This message cannot be forwarded or replicated', '')
    message = event.message
    if parse_trade_message_final(message)['validity']:
        await client_tg.send_message(
            entity=destination_chat,
            message=txt
        )
    print('Forwarded text message')


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
        sleep(1)
        await client_tg.send_message(
            entity=0,
            message=txt
        )
        print('Forwarded text message')
    elif is_similar_to_signal_TP(txt):
        await client_tg.send_message(
            entity=destination_chat,
            message=txt
        )
        sleep(1)
        await client_tg.send_message(
            entity=0,
            message=txt
        )
        print('Forwarded text message')


@client_tg.on(events.NewMessage(chats=0))
async def normal_handler_1(event):
    txt = str(event.message.to_dict()['message'])
    is_signal = is_trading_signal(txt)
    if is_signal:
        await client_tg.send_message(
            entity=destination_chat,
            message=clean_message(txt)
        )
        sleep(1)
        await client_tg.send_message(
            entity=0,
            message=clean_message(txt)
        )


source_chat_id = 0
destination_chat_id = 0


@client_tg.on(events.NewMessage(chats=source_chat_id))
async def normal_handler_1(event):
    message = event.message
    txt = message.message

    if message.media:
        await client_tg.send_message(
            entity=destination_chat_id,
            message=txt,
            file=message.media
        )
    else:
        await client_tg.send_message(
            entity=destination_chat_id,
            message=txt
        )


client_tg.start()
client_tg.run_until_disconnected()
