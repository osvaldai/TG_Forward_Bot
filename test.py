import re

import re




# Example usage
test_message = """🔴 TRADE - LINK / USDT ( Futures ) 

👉 Type - Long
👉 Mode - Isolated
👉 Leverage- 2X to 3X ( Recommend)

📌Buy Zone - 20.7$  to 20.5$

🎯Target

1  21.0$
2. 21.5$
3. 22.0$
4. 22.2$


🛑Stop loss 19$ -( SL Must Use )

🔥Disclaimer 👉 This is my personal analysis for educational purposes , Buy/Sell/Trade at your own risk. I am not a financial Advisor"""

parsed_message = parse_trade_message_final(test_message)
print(parsed_message)
