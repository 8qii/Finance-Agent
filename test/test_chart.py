import base64
from finance_agent.tools.chart import generate_price_chart

def test_generate_price_chart_simple():
    values = [1, 2, 3, 4, 5]
    result = generate_price_chart(values)
    assert isinstance(result, str)
    assert len(result) > 100  # base64 string

def test_generate_price_chart_with_labels():
    values = [10, 20, 30]
    labels = ["Day1", "Day2", "Day3"]
    result = generate_price_chart(values, labels)
    assert isinstance(result, str)
    decoded = base64.b64decode(result)
    assert decoded.startswith(b"\x89PNG")  # PNG header

def test_generate_price_chart_empty_values():
    try:
        generate_price_chart([])
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "values required" in str(e)
