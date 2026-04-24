import requests

from app.adanos_market_sentiment import fetch_adanos_market_sentiment, is_adanos_configured


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("bad response")

    def json(self):
        return self.payload


def test_is_adanos_configured_requires_non_empty_key():
    assert is_adanos_configured({"ADANOS_API_KEY": "secret"}) is True
    assert is_adanos_configured({"ADANOS_API_KEY": ""}) is False
    assert is_adanos_configured({}) is False


def test_fetch_adanos_market_sentiment_is_fail_open_without_key():
    def forbidden_call(*args, **kwargs):
        raise AssertionError("network call should not happen")

    data = fetch_adanos_market_sentiment("TSLA", {}, http_get=forbidden_call)

    assert data["enabled"] is False
    assert data["sources"] == []
    assert "Add an Adanos API key" in data["message"]


def test_fetch_adanos_market_sentiment_normalizes_partial_source_responses():
    payloads = {
        "reddit": {
            "buzz_score": 71.4,
            "sentiment_score": 0.32,
            "mentions": 182,
            "bullish_pct": 64.5,
            "bearish_pct": 11.2,
            "trend": "rising",
        },
        "x": {
            "buzz_score": 58.1,
            "sentiment_score": -0.14,
            "mentions": 94,
            "bullish_pct": 36.0,
            "bearish_pct": 28.0,
            "trend": "falling",
        },
        "news": None,
        "polymarket": {
            "buzz_score": 49.0,
            "sentiment_score": 0.08,
            "trade_count": 21,
            "market_count": 4,
            "bullish_pct": 51.0,
            "bearish_pct": 49.0,
            "trend": "stable",
        },
    }

    def fake_get(url, headers=None, timeout=None):
        assert headers == {"X-API-Key": "secret"}
        assert timeout == 12
        for slug, payload in payloads.items():
            if f"/{slug}/stocks/v1/stock/" in url:
                if payload is None:
                    raise ValueError("bad payload")
                return DummyResponse(payload)
        raise AssertionError(f"unexpected url {url}")

    data = fetch_adanos_market_sentiment(
        "tsla",
        {
            "ADANOS_API_KEY": "secret",
            "ADANOS_BASE_URL": "https://api.adanos.org/",
            "ADANOS_TIMEOUT_SECONDS": "12",
        },
        http_get=fake_get,
    )

    assert data["enabled"] is True
    assert data["ticker"] == "TSLA"
    assert [source["slug"] for source in data["sources"]] == ["reddit", "x", "polymarket"]
    assert data["unavailable_sources"] == ["News"]
    assert data["sources"][0]["metrics"][0] == {"label": "Buzz", "value": "71.4"}
    assert data["sources"][2]["metrics"][2] == {"label": "Trades", "value": "21"}


def test_fetch_adanos_market_sentiment_ignores_sources_without_metrics():
    def fake_get(url, headers=None, timeout=None):
        return DummyResponse({"trend": "stable"})

    data = fetch_adanos_market_sentiment(
        "AAPL",
        {"ADANOS_API_KEY": "secret"},
        http_get=fake_get,
    )

    assert data["enabled"] is True
    assert data["sources"] == []
    assert len(data["unavailable_sources"]) == 4
    assert "No Adanos sentiment data" in data["message"]


def test_fetch_adanos_market_sentiment_falls_back_to_default_base_url():
    captured_urls = []

    def fake_get(url, headers=None, timeout=None):
        captured_urls.append(url)
        return DummyResponse(
            {
                "buzz_score": 44.0,
                "sentiment_score": 0.1,
                "mentions": 12,
                "trend": "stable",
            }
        )

    data = fetch_adanos_market_sentiment(
        "msft",
        {"ADANOS_API_KEY": "secret", "ADANOS_BASE_URL": "   "},
        http_get=fake_get,
    )

    assert data["enabled"] is True
    assert captured_urls[0].startswith("https://api.adanos.org/")


def test_fetch_adanos_market_sentiment_marks_request_failures_unavailable():
    def fake_get(url, headers=None, timeout=None):
        if "/reddit/" in url:
            raise requests.Timeout("slow")
        return DummyResponse(
            {
                "buzz_score": 52.5,
                "sentiment_score": 0.05,
                "mentions": 25,
                "trend": "stable",
            }
        )

    data = fetch_adanos_market_sentiment(
        "NVDA",
        {"ADANOS_API_KEY": "secret"},
        http_get=fake_get,
    )

    assert data["enabled"] is True
    assert "Reddit" in data["unavailable_sources"]
    assert [source["slug"] for source in data["sources"]] == ["x", "news", "polymarket"]
