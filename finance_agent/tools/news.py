# finance_agent/tools/news.py
from typing import Dict, Any, Optional
import requests, os, logging

logger = logging.getLogger(__name__)

# SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
SERPAPI_KEY="d836f2f5a4eb9745402cc34aec553a84052c8c4112710812a61d39727ef584af"

def search_news(query: Optional[str] = None, ticker: Optional[str] = None) -> Dict[str, Any]:
    """
    Search financial news by query or ticker.
    """
    if not query and ticker:
        query = f"{ticker} stock news"

    if not query:
        return {"error": "query or ticker required", "results": []}

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_news",
        "q": f"{query}",
        "api_key": SERPAPI_KEY,
        "hl": "en",   # hoặc "vi"
        "gl": "us"    # hoặc "vn"
}


    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        news = []
        for item in data.get("news_results", []):
            news.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "date": item.get("date"),
                "snippet": item.get("snippet"),
            })
        return {"query": query, "results": news}
    except Exception as e:
        logger.error("search_news failed: %s", e)
        return {"query": query, "results": [], "error": str(e)}
