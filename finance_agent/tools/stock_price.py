# finance_agent/tools/stock_price.py
from __future__ import annotations
import datetime
import logging
import os
import certifi
import ssl
from typing import Dict, Any

logger = logging.getLogger(__name__)

os.environ["SSL_CERT_FILE"] = certifi.where()
ssl._create_default_https_context = ssl._create_unverified_context 

USE_YFINANCE = False
try:
    import yfinance as yf  # type: ignore
    USE_YFINANCE = True
except Exception:
    logger.info("yfinance not available; stock_price tool will use mock fallback.")


def _build_result(
    ticker: str,
    price: Any,
    currency: str | None,
    source: str,
    error: str | None = None,
) -> Dict[str, Any]:
    return {
        "ticker": ticker,
        "price": price,
        "currency": currency,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "source": source,
        "error": error,
    }


def _detect_currency(symbol: str) -> str:
    """Infer currency from ticker suffix (VN, HM, HN = VND)."""
    if symbol.endswith((".VN", ".HM", ".HN")):
        return "VND"
    return "USD"


def _normalize_symbol(symbol: str) -> str:
    """
    Normalize ticker for consistency.
    Just uppercase and strip spaces (do not force .VN).
    """
    return symbol.strip().upper()


def get_stock_price(
    ticker: str = None,
    stock_symbol: str = None,
    stock_ticker: str = None,
) -> Dict[str, Any]:
    """
    Get latest market price for a stock.
    Accepts multiple argument names (ticker, stock_symbol, stock_ticker).
    Returns structured dict.
    """
    symbol = ticker or stock_symbol or stock_ticker
    if not symbol or not isinstance(symbol, str):
        return _build_result(
            symbol or "",
            None,
            None,
            "invalid",
            "ticker/stock_symbol/stock_ticker is required",
        )

    norm_symbol = _normalize_symbol(symbol)

    if USE_YFINANCE:
        # Try as-is and then with .VN fallback if no suffix
        candidates = [norm_symbol]
        if "." not in norm_symbol:
            candidates.append(norm_symbol + ".VN")

        for try_sym in candidates:
            try:
                t = yf.Ticker(try_sym)
                hist = t.history(period="1d")
                if hist is not None and not hist.empty:
                    price = float(hist["Close"].iloc[-1])
                    currency = _detect_currency(try_sym)
                    return _build_result(try_sym, price, currency, "yfinance", None)
            except Exception as e:
                logger.error("yfinance attempt failed for %s: %s", try_sym, e)
                # retry with certifi fix
                try:
                    os.environ["SSL_CERT_FILE"] = certifi.where()
                    t = yf.Ticker(try_sym)
                    hist = t.history(period="1d")
                    if hist is not None and not hist.empty:
                        price = float(hist["Close"].iloc[-1])
                        currency = _detect_currency(try_sym)
                        return _build_result(try_sym, price, currency, "yfinance", None)
                except Exception as e2:
                    logger.error("yfinance retry failed for %s: %s", try_sym, e2)
                # unverified HTTPS fallback
                try:
                    logger.warning("Attempting unverified HTTPS request for yfinance (debug only).")
                    ssl._create_default_https_context = ssl._create_unverified_context  # type: ignore
                    t = yf.Ticker(try_sym)
                    hist = t.history(period="1d")
                    if hist is not None and not hist.empty:
                        price = float(hist["Close"].iloc[-1])
                        currency = _detect_currency(try_sym)
                        return _build_result(try_sym, price, currency, "yfinance-unverified", None)
                except Exception as e3:
                    logger.error("Unverified yfinance attempt also failed for %s: %s", try_sym, e3)

        return _build_result(norm_symbol, None, None, "yfinance", "no data for symbol or .VN")

    # fallback mock
    logger.info("Returning mock price for %s (yfinance not available or failed).", norm_symbol)
    return _build_result(norm_symbol, 12.34, "USD", "mock", "mock fallback used")
