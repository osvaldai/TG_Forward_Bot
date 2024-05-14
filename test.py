import re


def clean_message(message: str) -> str:
    # Define patterns to remove from the message
    remove_patterns = [
        r"Disclaimer: Carries High Risk",
        r"Registration"
    ]

    # Remove specified lines
    for pattern in remove_patterns:
        message = re.sub(pattern, '', message, flags=re.MULTILINE).strip()

    return message


def is_trading_signal(message: str) -> bool:
    # Clean the message
    message = clean_message(message)

    # Print the cleaned message for debugging
    print("Cleaned Message:\n", message)

    # Define simpler patterns to look for in the message
    signal_patterns = [
        r"#\w+/\w+",  # Symbol pattern e.g. #BEAM/USDT
        r"Signal Type: \w+ \(\w+\)",  # Signal type pattern e.g. Signal Type: Regular (Long)
        r"Entry Around:\s*\d+\.\d+",  # Entry price pattern e.g. Entry Around: 0.022663
        r"Take-Profit Targets:",  # Take-Profit targets pattern
        r"Stop Targets:",  # Stop targets pattern
    ]

    # Check if all patterns are present in the message
    for pattern in signal_patterns:
        if not re.search(pattern, message):
            print(f"Pattern not found: {pattern}")
            return False

    return True


# Example usage
message = """Coin: $SXP/USDT

Direction: LONG
Leverage: 20x (Cross)
-----------------------------------

ENTRY:
1) 0,415
2) 0,39425
3) 0,3735
4) 0,35275
•
TAKE-PROFIT:
1) 0,425375
2) 0,43575
3) 0,446125
4) 0,4565
5) 0,47725
6) 0,498
7) 0,51875
8) 0,5395
9) 0,581
10) 0,6225
•
⛔ STOP-LOSS: 0,31125"""

is_signal = is_trading_signal(message)
print(is_signal)  # Should print: True
