from finance_agent.tools.ratios import calculate_ratios

def test_calculate_ratios_mock():
    result = calculate_ratios("AAPL")
    assert "ratios" in result

def test_calculate_ratios_with_financials():
    financials = {
        "revenue": 1000,
        "net_income": 200,
        "total_equity": 500,
        "market_price": 10,
        "shares_outstanding": 100,
    }
    result = calculate_ratios("AAPL", financials)
    assert "ratios" in result
    assert result["ratios"]["roe"] == 200 / 500
