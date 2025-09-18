from finance_agent.tools.stock_price import get_stock_price

def test_get_stock_price_mock():
    result = get_stock_price("AAPL")
    assert "ticker" in result
    assert "price" in result

def test_get_stock_price_invalid():
    result = get_stock_price("")
    assert result["error"] is not None
