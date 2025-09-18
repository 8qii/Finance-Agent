from finance_agent.tools.stock_symbol import get_stock_symbol

def test_get_stock_symbol_mock():
    result = get_stock_symbol("Apple")
    assert "company_name" in result
    assert "ticker" in result or result["error"] is not None

def test_get_stock_symbol_empty():
    result = get_stock_symbol("")
    assert "error" in result
