function update_price_color() {
    var tickers = document.getElementsByClassName("ticker_item");
    for (i=0; i<tickers.length; i++) {
        if (tickers[i].querySelector("span").innerHTML.includes("+") == true) {
            tickers[i].querySelector("span").style.color="#26a69a"
        }

        else {
            tickers[i].querySelector("span").style.color="#ef5350"
        }
    }
}

function show_ticker_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "ticker_price"
}

function show_reddit_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "reddit_analysis"
}

function show_google_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "google_analysis"
}

function show_industry_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "industry"
}