# manual_test_tools.py
from finance_agent.tools.chart import generate_price_chart
from finance_agent.tools.fundamentals import get_fundamentals
from finance_agent.tools.google_search import google_search
from finance_agent.tools.news import search_news
from finance_agent.tools.pdf_parse import parse_financial_report
from finance_agent.tools.ratios import calculate_ratios
from finance_agent.tools.stock_price import get_stock_price
from finance_agent.tools.stock_symbol import get_stock_symbol

print("=== Manual Tool Tests ===")

# 1. Chart
print("\n[Chart] generate_price_chart")
values = [10, 20, 30, 25, 40]
labels = ["Day1", "Day2", "Day3", "Day4", "Day5"]
chart_b64 = generate_price_chart(values, labels)
print("Output (base64, first 60 chars):", chart_b64[:60])

# 2. Fundamentals
print("\n[Fundamentals] get_fundamentals")
fundamentals = get_fundamentals("AAPL")
print("Output:", fundamentals)

# 3. Google Search
print("\n[Google Search] google_search")
search_res = google_search("Mã cổ phiếu của FPT")
print("Output:", search_res)

# 4. News
print("\n[News] search_news")
news_res = search_news("Apple")
print("Output:", news_res)

# 5. PDF Parse
print("\n[PDF Parse] parse_financial_report")
pdf_res = parse_financial_report("dummy_report.pdf", ["Summary", "Balance Sheet"])
print("Output:", pdf_res)

# 6. Ratios
print("\n[Ratios] calculate_ratios")
ratios_res = calculate_ratios("AAPL", {
    "revenue": 1000000,
    "net_income": 200000,
    "total_equity": 500000,
    "market_price": 150,
    "shares_outstanding": 10000
})
print("Output:", ratios_res)

# 7. Stock Price
print("\n[Stock Price] get_stock_price")
price_res = get_stock_price(ticker="FPT.VN")
print("Output:", price_res)

# 8. Stock Symbol
print("\n[Stock Symbol] get_stock_symbol")
symbol_res = get_stock_symbol("Apple", country="US")
print("Output:", symbol_res)
