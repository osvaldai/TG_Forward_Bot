import re


def is_trading_signal(message: str) -> bool:
    # Define individual patterns
    pair_pattern = re.search(r"#\w+/\w+", message)
    signal_type_pattern = re.search(r"Signal Type:\s*(Regular|Scalp|Swing) \((Long|Short)\)", message)
    entry_target_pattern = re.search(r"Entry Targets:\s*\d+\.\d+", message)
    take_profit_pattern = re.search(r"Take-Profit Targets:\s*(\d+\) \d+\.\d+\s*)+", message)
    # stop_targets_pattern = re.search(r"Stop Targets:\s*\d+%-\d+%", message)

    # Check if all patterns are found in the message
    if (pair_pattern and signal_type_pattern and entry_target_pattern and
            take_profit_pattern):
        return True

    return False


# Example usage
message = """⚡️⚡️ #ARPA/USDT ⚡️⚡️
Exchanges: Bingx 👉

Signal Type: Regular (Long)
Leverage: Cross (20х)

Entry Targets:
0.07795

Take-Profit Targets:
1) 0.07912
2) 0.07990
3) 0.08068
4) 0.08185
5) 0.08263
6) 0.08380
7) 🚀🚀🚀

Stop Targets:
5-10%"""

print(is_trading_signal(message))  # Output: True
