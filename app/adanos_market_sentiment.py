import math
from typing import Any, Dict, List, Mapping, Optional

import requests


ADANOS_SOURCE_SPECS = (
    {
        "slug": "reddit",
        "label": "Reddit",
        "description": "Retail investor discussion across stock subreddits.",
        "path": "reddit/stocks/v1/stock/{ticker}",
    },
    {
        "slug": "x",
        "label": "X / FinTwit",
        "description": "Social momentum from finance-focused X chatter.",
        "path": "x/stocks/v1/stock/{ticker}",
    },
    {
        "slug": "news",
        "label": "News",
        "description": "News sentiment from financial publishers and headlines.",
        "path": "news/stocks/v1/stock/{ticker}",
    },
    {
        "slug": "polymarket",
        "label": "Polymarket",
        "description": "Prediction-market positioning and activity for stock-linked markets.",
        "path": "polymarket/stocks/v1/stock/{ticker}",
    },
)

DEFAULT_ADANOS_BASE_URL = "https://api.adanos.org"
DEFAULT_ADANOS_TIMEOUT_SECONDS = 8


def is_adanos_configured(config: Optional[Mapping[str, Any]]) -> bool:
    if not config:
        return False
    return bool(str(config.get("ADANOS_API_KEY", "")).strip())


def _safe_float(value: Any) -> Optional[float]:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(out) or math.isinf(out):
        return None
    return out


def _coerce_timeout(config: Optional[Mapping[str, Any]]) -> int:
    try:
        timeout = int((config or {}).get("ADANOS_TIMEOUT_SECONDS", DEFAULT_ADANOS_TIMEOUT_SECONDS))
    except (TypeError, ValueError):
        timeout = DEFAULT_ADANOS_TIMEOUT_SECONDS
    return max(timeout, 1)


def _base_url(config: Optional[Mapping[str, Any]]) -> str:
    value = str((config or {}).get("ADANOS_BASE_URL", "")).strip()
    if not value:
        value = DEFAULT_ADANOS_BASE_URL
    return value.rstrip("/")


def _unavailable_source_labels() -> List[str]:
    return [spec["label"] for spec in ADANOS_SOURCE_SPECS]


def _metric_entry(label: str, value: Any, decimals: int = 1, suffix: str = "") -> Optional[Dict[str, Any]]:
    numeric_value = _safe_float(value)
    if numeric_value is None:
        if value in (None, "", "N/A"):
            return None
        display_value = str(value)
    else:
        if decimals == 0:
            display_value = f"{int(round(numeric_value)):,}"
        else:
            display_value = f"{numeric_value:.{decimals}f}"
            if "." in display_value:
                display_value = display_value.rstrip("0").rstrip(".")
    return {"label": label, "value": f"{display_value}{suffix}"}


def _build_metrics(source_slug: str, payload: Mapping[str, Any]) -> List[Dict[str, Any]]:
    metrics: List[Dict[str, Any]] = []

    for entry in (
        _metric_entry("Buzz", payload.get("buzz_score")),
        _metric_entry("Sentiment", payload.get("sentiment_score"), decimals=2),
        _metric_entry(
            "Trades" if source_slug == "polymarket" else "Mentions",
            payload.get("trade_count") if source_slug == "polymarket" else payload.get("mentions"),
            decimals=0,
        ),
        _metric_entry("Bullish", payload.get("bullish_pct"), suffix="%"),
        _metric_entry("Bearish", payload.get("bearish_pct"), suffix="%"),
        _metric_entry("Markets", payload.get("market_count"), decimals=0)
        if source_slug == "polymarket"
        else None,
    ):
        if entry:
            metrics.append(entry)
    return metrics


def normalize_adanos_source(spec: Mapping[str, str], payload: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(payload, Mapping):
        return None

    metrics = _build_metrics(spec["slug"], payload)
    if not metrics:
        return None

    return {
        "slug": spec["slug"],
        "label": spec["label"],
        "description": spec["description"],
        "trend": payload.get("trend") or "N/A",
        "sentiment_score": _safe_float(payload.get("sentiment_score")),
        "buzz_score": _safe_float(payload.get("buzz_score")),
        "mentions": payload.get("mentions"),
        "trade_count": payload.get("trade_count"),
        "market_count": payload.get("market_count"),
        "bullish_pct": _safe_float(payload.get("bullish_pct")),
        "bearish_pct": _safe_float(payload.get("bearish_pct")),
        "metrics": metrics,
    }


def fetch_adanos_market_sentiment(
    ticker_selected: str,
    config: Optional[Mapping[str, Any]],
    http_get=requests.get,
) -> Dict[str, Any]:
    ticker = str(ticker_selected or "").upper()
    if not is_adanos_configured(config):
        return {
            "enabled": False,
            "ticker": ticker,
            "message": "Add an Adanos API key in Setup to enable cross-source market sentiment.",
            "sources": [],
            "unavailable_sources": _unavailable_source_labels(),
        }

    headers = {"X-API-Key": str(config.get("ADANOS_API_KEY")).strip()}
    base_url = _base_url(config)
    timeout = _coerce_timeout(config)

    sources = []
    unavailable_sources = []
    for spec in ADANOS_SOURCE_SPECS:
        url = f"{base_url}/{spec['path'].format(ticker=ticker)}"
        try:
            response = http_get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            normalized = normalize_adanos_source(spec, response.json())
            if normalized:
                sources.append(normalized)
            else:
                unavailable_sources.append(spec["label"])
        except (requests.RequestException, ValueError):
            unavailable_sources.append(spec["label"])

    return {
        "enabled": True,
        "ticker": ticker,
        "message": "" if sources else "No Adanos sentiment data is available for this ticker right now.",
        "sources": sources,
        "unavailable_sources": unavailable_sources,
    }
