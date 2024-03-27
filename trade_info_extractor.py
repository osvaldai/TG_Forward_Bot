import re


def parse_trade_message(message):
    """Bitcoin premium Channel 1001736278884"""
    """
    Parses the trade message and extracts information such as trade side, trading pair,
    entry points, take profits, stop loss, leverage, and funds.

    :param message: The trade message string.
    :return: A dictionary with parsed trade information.
    """
    info = {}

    # Extracting trade side (Long or Short)
    trade_side_match = re.search(r'(LONG|SHORT)', message)
    info['trade_side'] = trade_side_match.group(0).upper() if trade_side_match else None

    # Extracting trading pair
    pair_match = re.search(r'([A-Z]{3,5}/[A-Z]{3,5})', message)
    info['trading_pair'] = str(pair_match.group(0)).replace('/', '') if pair_match else None

    # Extracting entry points
    entries = re.findall(r'Entry\s*(\d+)\)\s*([\d\.]+)', message)
    info['entries'] = {float(point[1]) for point in entries}

    take_profits = re.findall(r'Take-Profit Targets:\s*((?:\d+\)\s*[\d\.-]+-?\s*\d+%?\s*)+)', message)
    if take_profits:
        tp_matches = re.findall(r'(\d+)\)\s*([\d\.]+)', take_profits[0])
        info['take_profits'] = {float(match[1]) for match in tp_matches}

    # Extracting stop loss
    stop_loss_match = re.search(r'Stop Loss:-\s*([\d\.]+)', message)
    info['stop_loss'] = float(stop_loss_match.group(1)) if stop_loss_match else None

    # Extracting leverage and fund usage
    leverage_fund_match = re.search(r'Use (\d+)X Leverage and (\d+)% Funds', message)
    if leverage_fund_match:
        info['leverage'] = int(leverage_fund_match.group(1))
        info['fund_usage'] = int(leverage_fund_match.group(2))

    return info


def is_trade_message(text):
    """Bitcoin premium Channel 1001736278884"""
    """
    Checks if the provided text contains a trade message, focusing on a broad range of trading terms.

    :param text: The text to be checked for trade messages.
    :return: True if a trade message is found, False otherwise.
    """
    # Updated pattern to include various trading-related terms
    pattern = r'#(\w+/\w+).*?(Entry|Take-Profit target|Profit|Period)'
    return bool(re.search(pattern, text, re.IGNORECASE))


def parse_trade_message_49(message):
    """rus fed premium channel 1001525644349"""
    # Regular expressions for each piece of data
    id_pattern = r"VIP Trade ID: #(\w+)"
    pair_pattern = r"Pair: \$(\w+/\w+)"
    direction_pattern = r"Direction: (⬆️LONG|⬇️SHORT)"
    entry_pattern = r"ENTRY : ([\d.]+) - ([\d.]+)"
    targets_pattern = r"🔘Target \d+ -([\d.]+)"
    stop_loss_pattern = r"🚫STOP LOSS: ([\d.]+)"

    # Extract data using regex
    trade_id = re.search(id_pattern, message)
    pair = re.search(pair_pattern, message)
    direction = re.search(direction_pattern, message)
    entry = re.search(entry_pattern, message)
    targets = re.findall(targets_pattern, message)
    stop_loss = re.search(stop_loss_pattern, message)

    # Validation and structuring
    trade_data = {}
    if trade_id and pair and direction and entry and targets and stop_loss:
        trade_data = {
            # "id": trade_id.group(1),
            "pair": pair.group(1),
            "direction": str(direction.group(1)).replace('⬆️', '').replace('⬇️', ''),
            "entry": {float(entry.group(1)), float(entry.group(2))},
            "targets": [float(target) for target in targets],
            "stop_loss": float(stop_loss.group(1))
        }
    return trade_data


def is_valid_trade_message_49(message):
    """rus fed premium channel 1001525644349"""
    # Simple string checks for trading pair, targets, and profit
    has_pair = "Pair: $" in message
    has_targets = "Target" in message
    has_profit = "Profit:" in message

    # Valid if all required components are present
    return has_pair and has_targets and has_profit


def parse_trading_signal(message):
    """vip crypto galaxy 1002143151446"""
    # Check if it's a trading signal
    if not ("Coin:" in message and "Direction:" in message):
        return None

    # Extracting details
    details = {'Trading Pair': str(re.search(r'Coin: (\$\w+/\w+)', message).group(1)).replace('$', '').replace('/', ''),
               'Direction': re.search(r'Direction: (\w+)', message).group(1),
               'Leverage': re.search(r'Leverage: (\d+x)', message).group(1)}

    # Entry Points
    entry_points = re.findall(r'ENTRY:\s*(.*?)\s*\•', message, re.DOTALL)
    details['Entry Points'] = re.findall(r'(\d+,\d+)', entry_points[0])

    # Take-Profit Points
    tp_points = re.findall(r'TAKE-PROFIT:\s*(.*?)\s*\•', message, re.DOTALL)
    details['Take-Profit Points'] = re.findall(r'(\d+,\d+)', tp_points[0])

    # Stop-Loss Point
    details['Stop-Loss Point'] = re.search(r'⛔ STOP-LOSS: (\d+,\d+)', message).group(1)

    return details


def is_valid_trading_summary(message):
    """vip crypto galaxy 1002143151446"""
    # Regular expression patterns for each component
    platform_pattern = r'(Binance Futures|ByBit USDT|KuCoin Futures|OKX Futures)'
    trading_pair_pattern = r'#\w+/USDT'
    profit_pattern = r'Profit: \d+(\.\d+)?%'
    period_pattern = r'Period: \d+ Days \d+ Hours \d+ Minutes'

    # Checking if all patterns are present in the message
    if re.search(platform_pattern, message) and \
            re.search(trading_pair_pattern, message) and \
            re.search(profit_pattern, message) and \
            re.search(period_pattern, message):
        return True
    else:
        return False


def parse_trade_message_1(message: str) -> dict:
    # Regular expression patterns
    pair_pattern = r"TRADE -\s*([A-Za-z/]+)\s*\( Futures \)"
    direction_pattern = r"Type -\s*(Long|Short)"
    entry_pattern = r"Buy Zone -\s*(\d+\.?\d*)\$\s*to\s*(\d+\.?\d*)\$"
    targets_pattern = r"🎯Target((?:\n\d+\.\s*\d+\.\d+\$)+)"
    stop_loss_pattern = r"🛑Stop loss\s*(\d+\.?\d*)\$"

    # Parsing
    result = {
        "validity": "False",
        "trading_pair": None,
        "trade_direction": None,
        "entry_point": [],
        "take_profits": [],
        "stop_loss": None
    }

    # Check if the message is a valid trade message
    if "TRADE -" in message and "🎯Target" in message:
        result["validity"] = "True"
        pair_match = re.search(pair_pattern, message)
        direction_match = re.search(direction_pattern, message)
        entry_match = re.search(entry_pattern, message)
        targets_match = re.search(targets_pattern, message)
        stop_loss_match = re.search(stop_loss_pattern, message)

        if pair_match:
            result["trading_pair"] = pair_match.group(1)
        if direction_match:
            result["trade_direction"] = direction_match.group(1)
        if entry_match:
            result["entry_point"] = [float(entry_match.group(1)), float(entry_match.group(2))]
        if targets_match:
            result["take_profits"] = [float(tp) for tp in re.findall(r"\d+\.\d+", targets_match.group(1))]
        if stop_loss_match:
            result["stop_loss"] = float(stop_loss_match.group(1))

    return result


def parse_trade_message_updated(message: str) -> dict:
    # Updated regular expression patterns
    pair_pattern = r"TRADE -\s*([A-Za-z/]+\s*/\s*[A-Za-z]+)\s*\( Futures \)"
    targets_pattern = r"🎯Target(?:\n\d+\.\s*(\d+\.\d+)\$)+"

    # Re-parsing with updated patterns
    result = parse_trade_message_1(message)

    # Update the pattern matching
    pair_match = re.search(pair_pattern, message)
    targets_match = re.findall(targets_pattern, message)

    if pair_match:
        result["trading_pair"] = pair_match.group(1).replace(" ", "")
    if targets_match:
        result["take_profits"] = targets_match

    return result


def parse_trade_message_final(message: str) -> dict:
    # Final regular expression pattern adjustment for take profits
    targets_pattern = r"\d+\.\s*(\d+\.\d+)\$"

    # Re-parsing with final patterns
    result = parse_trade_message_updated(message)

    # Update the pattern matching for take profits
    targets_match = re.findall(targets_pattern, message)
    if targets_match:
        result["take_profits"] = targets_match

    return result
