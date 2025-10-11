import yfinance as yf

def debug_fundamentals(ticker: str):
    t = yf.Ticker(ticker)

    print("=" * 50)
    print(f"🔍 Debugging fundamentals for {ticker}")
    print("=" * 50)

    # --- Info ---
    print("\n--- INFO ---")
    info = t.info
    for k in ["marketCap", "sharesOutstanding", "sector", "country"]:
        print(f"{k}: {info.get(k)}")

    # --- Income Statement ---
    print("\n--- INCOME STATEMENT ---")
    try:
        fin = t.financials
        print("Index:", fin.index)
        print("Columns:", fin.columns)
        print(fin.head(20))
    except Exception as e:
        print("Error fetching income statement:", e)

    # --- Balance Sheet ---
    print("\n--- BALANCE SHEET ---")
    try:
        bs = t.balance_sheet
        print("Index:", bs.index)
        print("Columns:", bs.columns)
        print(bs.head(20))
    except Exception as e:
        print("Error fetching balance sheet:", e)

    print("\n--- Candidate Equity Keys ---")
    candidates = [
        "Total Stockholder Equity",
        "Total Stockholders Equity",
        "Total Equity",
        "Ordinary Shares Equity",
        "Common Stock Equity",
    ]
    try:
        bs = t.balance_sheet
        for c in candidates:
            if c in bs.index:
                val = bs.loc[c].dropna()
                if not val.empty:
                    print(f"{c}: {val.iloc[0]} (latest)")
    except Exception as e:
        print("Error while scanning equity keys:", e)


if __name__ == "__main__":
    # Anh thử với Apple trước
    debug_fundamentals("AAPL")

    # Nếu muốn test thêm
    debug_fundamentals("MSFT")
    debug_fundamentals("VNM.VN")  # thử với Vinamilk nếu có
