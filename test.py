import re


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


# Example usage
message = """
📍SIGNAL ID: #1366📍
COIN: $OXT/USDT (3-5x)
Direction: LONG📈
➖➖➖➖➖➖➖
Breakout retest

ENTRY: 0.099 - 0.10775
OTE: 0.104

TARGETS
Short Term: 0.1086 - 0.1093 - 0.112 - 0.115 - 0.118
Mid Term: 0.121 - 0.125 - 0.130 - 0.137 - 0.146

STOP LOSS: 0.09302
➖➖➖➖➖➖➖
This message cannot be forwarded or replicated
- Binance Killers®
"""

extracted_info = extract_trading_info(message)
print(extracted_info)
