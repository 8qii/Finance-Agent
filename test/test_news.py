from finance_agent.tools.news import search_news

def test_search_news_mock():
    result = search_news("Apple")
    assert "query" in result
    assert "items" in result
    assert isinstance(result["items"], list)
    assert "title" in result["items"][0]
