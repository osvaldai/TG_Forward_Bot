import re


def is_trading_signal(message: str) -> bool:
    # Define individual patterns
    pair_pattern = re.search(r"#\w+/\w+", message)
    signal_type_pattern = re.search(r"Signal Type:\s*(Regular|Scalp|Swing) \((Long|Short)\)", message)
    entry_target_pattern = re.search(r"Entry Around:\s*\d+\.\d+", message)
    take_profit_pattern = re.findall(r"\d+\)\s*\d+\.\d+", message)

    # Check if all patterns are found in the message
    if (pair_pattern and signal_type_pattern and entry_target_pattern and
            len(take_profit_pattern) >= 1):
        return True

    return False


# Example usage
message = """⚡️⚡️ #GTC/USDT ⚡️⚡️
Exchanges: Bingx Recommended 👉

Signal Type: Regular (Short)
Leverage: Cross (20х)

Entry Around:
1.634

Take-Profit Targets:
1) 1.60949
2) 1.59315
3) 1.57681
4) 1.55230
5) 1.53596
6) 1.51145
7) 🚀🚀🚀

Stop Targets:
5-10%"""

print(is_trading_signal(message))  # Output: True
