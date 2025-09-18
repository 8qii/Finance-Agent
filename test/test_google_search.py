from finance_agent.tools.google_search import google_search

def test_google_search_mock():
    query = "Apple stock ticker"
    result = google_search(query)
    assert "query" in result
    assert isinstance(result["results"], list)
    assert any("Mock" in str(r.get("title")) for r in result["results"])
