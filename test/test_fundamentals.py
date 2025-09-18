from finance_agent.tools.fundamentals import get_fundamentals

def test_get_fundamentals_with_ticker():
    result = get_fundamentals("AAPL")
    assert "ticker" in result
    assert "snapshot" in result or "error" in result

def test_get_fundamentals_no_ticker():
    result = get_fundamentals("")
    assert "error" in result
